#!/usr/bin/env python3
import argparse
import sys, os

from config import BenchConfig, ModelDescription, ModelSize, config_logger
from supportllm import LlamaCppBinary
from supportmodel import GGUFModel
from downloadsupport import Checksums

DEFAULT_ENGINE_LIST = ['vulkan', 'openblas']
DEFAULT_ENGINE_OS = 'win'
DEFAULT_ENGINE_ARCH = 'x64'
DEFAULT_LLAMA_CPP_VERSION = '4321'

MODEL_DESCRIPTIONS: list[ModelDescription] = [
    ModelDescription(
        size=ModelSize.TINY,
        name="qwen2.5 / 1.5B / f16",
        url="https://huggingface.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/Qwen2.5-1.5B-Instruct-f16.gguf"
    ),
    ModelDescription(
        size=ModelSize.TINY,
        name="qwen2.5 / 1.5B / q8",
        url="https://huggingface.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/Qwen2.5-1.5B-Instruct-Q8_0.gguf"
    ),
    ModelDescription(
        size=ModelSize.TINY,
        name="qwen2.5 / 1.5B / q4",
        url="https://huggingface.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/Qwen2.5-1.5B-Instruct-Q4_0.gguf"
    ),
    ModelDescription(
        size=ModelSize.SMALL,
        name="qwen2.5 / 7B / q8",
        url="https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q8_0.gguf"
    ),
    ModelDescription(
        size=ModelSize.SMALL,
        name="qwen2.5 / 7B / q4",
        url="https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q4_0.gguf"
    ),
]


log = config_logger()


def exit(message: str, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def main():
    bench_config = process_args()
    print(bench_config)

    Checksums.init()

    llamacpps = [
        LlamaCppBinary(
            engine=e,
            os=bench_config.engine_os,
            arch=bench_config.engine_arch,
            llama_cpp_version=bench_config.llama_cpp_version,
            working_dir=bench_config.working_dir
        ) for e in bench_config.engine_list
    ]

    models = [
        GGUFModel(md, bench_config.working_dir)
        for md in MODEL_DESCRIPTIONS
    ]

    for md in models:
        if not md.download():
            exit("Fatal error")

    for llamacpp in llamacpps:
        if not llamacpp.download():
            exit("Fatal error")
        if not llamacpp.extract():
            exit("Fatal error")


def process_args():
    parser = argparse.ArgumentParser(
        prog='llmbench',
        epilog=f"See the Assets section in llama.cpp Releases (https://github.com/ggerganov/llama.cpp/releases) for what engines, OSes and CPU architectures are supported.\nDefault={DEFAULT_ENGINE_LIST} {DEFAULT_ENGINE_OS} {DEFAULT_ENGINE_ARCH}.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    engine_list = []

    parser.add_argument('-E', '--enable', action='append', default=DEFAULT_ENGINE_LIST, help='Enable an llama.cpp engine')
    parser.add_argument('-D', '--disable', action='append', help='Disable an llama.cpp engine')
    parser.add_argument('-O', '--os', default=DEFAULT_ENGINE_OS, help='Operating system')
    parser.add_argument('-A', '--arch', default=DEFAULT_ENGINE_ARCH, help='CPU architecture')
    parser.add_argument('-L', '--llama_cpp_version', default=DEFAULT_LLAMA_CPP_VERSION, help='llama.cpp release version')
    parser.add_argument('-d', '--working_dir', default='.', help='Working directory (10-15 GB of disk space needed)')
    parser.add_argument('-c', '--cleanup', action='store_true', default=False, help="Delete downloaded files from the working_dir")
    args = parser.parse_args()
    if args.enable:
        for engine in args.enable:
            if not engine in engine_list:
                engine_list.append(engine)
    if args.disable:
        for engine in args.disable:
            if engine in engine_list:
                engine_list.remove(engine)
    bench_config = BenchConfig(
        engine_list = engine_list,
        engine_os = args.os,
        engine_arch = args.arch,
        llama_cpp_version = args.llama_cpp_version,
        working_dir = args.working_dir,
        cleanup = args.cleanup,
    )
    return bench_config


if __name__ == '__main__':
    main()
