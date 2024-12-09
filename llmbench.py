#!/usr/bin/env python3
import argparse
import sys, os

from config import BenchConfig

DEFAULT_ENGINE_LIST = ['vulkan', 'openblas']
DEFAULT_ENGINE_OS = 'win'
DEFAULT_ENGINE_ARCH = 'x64'
DEFAULT_LLAMA_CPP_VERSION = '4295'

LLM_TEXT_MODEL_URL = 'https://huggingface.co/bartowski/Qwen2.5-3B-GGUF/resolve/main/Qwen2.5-3B-Q4_K_L.gguf'

bench_config: BenchConfig = None

def main():
    process_args()


def process_args():
    global bench_config
    parser = argparse.ArgumentParser(
        prog='llmbench'
    )

    engine_list = DEFAULT_ENGINE_LIST[:]

    parser.add_argument('-E', '--enable', action='append')
    parser.add_argument('-D', '--disable', action='append')
    parser.add_argument('-O', '--os', default=DEFAULT_ENGINE_OS)
    parser.add_argument('-A', '--arch', default=DEFAULT_ENGINE_ARCH)
    parser.add_argument('-L', '--llama_cpp_version', default=DEFAULT_LLAMA_CPP_VERSION)
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
    )
    print(bench_config)


if __name__ == '__main__':
    main()
