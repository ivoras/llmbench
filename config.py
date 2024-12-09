from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class BenchConfig:
    engine_list: list[str]
    engine_os: str
    engine_arch: str
    llama_cpp_version: str

