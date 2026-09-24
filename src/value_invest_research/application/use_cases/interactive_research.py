"""One serialized edit/research/publication cycle, provider- and I/O-independent."""
from threading import RLock, Event
from concurrent.futures import ThreadPoolExecutor

from value_invest_research.domain.interactive_research import propose_edit, tree_version
from value_invest_research.ports.interactive_research import InteractiveResearchRepository, InteractiveResearchRunner

ACTIVE = {"queued", "running", "validating", "publishing"}


class InteractiveResearch:
    def __init__(self, repository: InteractiveResearchRepository, runner: InteractiveResearchRunner):
        self.repository, self.runner = repository, runner
        self.lock, self.cancelled = RLock(), Event()
        self.pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="research")

    def state(self):
        with self.lock:
            tree = self.repository.tree()
            return {"tree": tree, "version": tree_version(tree), "job": self.repository.current_job()}

    def preview(self, request):
        with self.lock:
            tree = self.repository.tree()
            if request.get("version") != tree_version(tree):
                raise ValueError("报告已被其他操作更新，请刷新后重试。")
            return propose_edit(tree, request)

    def process(self):
        with self.lock:
            return self.repository.process()

    def submit(self, request):
        with self.lock:
            job = self.repository.current_job()
            if job and job["status"] in ACTIVE:
                raise ValueError("已有研究正在运行，请等待或取消后再编辑。")
            proposal = self.preview(request)
            job = self.repository.prepare(proposal)
            self.cancelled.clear()
            self.pool.submit(self._execute, job)
            return job

    def cancel(self):
        with self.lock:
            job = self.repository.current_job()
            if not job or job["status"] not in ACTIVE:
                raise ValueError("没有正在执行的研究。")
            self.cancelled.set()
            job["message"] = "已请求取消；现有报告保持不变。"
            self.repository.save_job(job)

    def _execute(self, job):
        def update(message, status="running"):
            with self.lock:
                job.update(status=status, message=message)
                self.repository.save_job(job)
        try:
            update("正在启动研究引擎，逐题检索与复核。")
            self.runner.run(job["workspace"], job, update, self.cancelled.is_set)
            if self.cancelled.is_set():
                raise InterruptedError("用户取消")
            update("正在检查问题范围、证据链、计划与报告；尚未覆盖正式报告。", "validating")
            with self.lock:
                if self.cancelled.is_set():
                    raise InterruptedError("用户取消")
                self.repository.validate_and_publish(job)
                update("报告已更新。研究不足的节点仍标注缺口，不等于投资结论通过。", "updated")
        except InterruptedError:
            update("研究已取消；草稿与执行记录保留，正式报告未变。", "cancelled")
        except Exception as exc:
            # Adapter exceptions are sanitized; never expose raw provider logs or credentials.
            update(str(exc)[:1000], "failed")

    def close(self):
        self.cancelled.set()
        self.pool.shutdown(wait=True)
