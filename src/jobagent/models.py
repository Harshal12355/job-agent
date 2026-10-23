from dataclasses import asdict, dataclass, field


@dataclass
class ApplyOption:
    url: str
    publisher: str
    board: str            # greenhouse | lever | ashby | workday | linkedin | indeed | employer | other
    automatable: bool


@dataclass
class Job:
    job_id: str           # <source>_<company>_<posting id>
    source: str           # jsearch | greenhouse | lever | ashby
    company: str
    title: str
    location: str
    remote: bool | None
    url: str              # where a human reads the posting
    posted_at: str | None # ISO 8601 UTC
    description: str
    apply_options: list[ApplyOption] = field(default_factory=list)
    salary_min: float | None = None
    salary_max: float | None = None

    @property
    def best_apply(self) -> ApplyOption | None:
        """Automatable ATS first, then the employer's own site, then anything else."""
        rank = {True: 0, False: 1}
        options = sorted(
            self.apply_options,
            key=lambda o: (rank[o.automatable], o.board not in ("employer",), o.board in ("linkedin", "indeed")),
        )
        return options[0] if options else None

    def to_dict(self) -> dict:
        data = asdict(self)
        best = self.best_apply
        data["best_apply"] = asdict(best) if best else None
        return data
