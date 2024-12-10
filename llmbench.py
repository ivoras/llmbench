#!/usr/bin/env python3
import argparse
import sys, os

from config import BenchConfig

DEFAULT_ENGINE_LIST = ['vulkan', 'openblas']
DEFAULT_ENGINE_OS = 'win'
DEFAULT_ENGINE_ARCH = 'x64'
DEFAULT_LLAMA_CPP_VERSION = '4295'

LLM_TEXT_MODEL_URL = 'https://huggingface.co/bartowski/Qwen2.5-3B-GGUF/resolve/main/Qwen2.5-3B-Q4_K_L.gguf'


def main():
    bench_config = process_args()
    print(bench_config)


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
    parser.add_argument('-d', '--working_dir', default='.', help='Working directory (5-10 GB of disk space needed)')
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
    )
    return bench_config


if __name__ == '__main__':
    main()
