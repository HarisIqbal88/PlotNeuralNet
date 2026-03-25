import os
import shutil
import subprocess
import sys


EXAMPLES = [
    'test_simple.py',
    'unet.py',
    'attention_unet.py',
    'transformer_encoder.py',
    'transunet.py',
]


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def compile_tex(tex_file, cwd):
    if not shutil.which('pdflatex'):
        return None, 'pdflatex not found, skip compile'
    result = run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex_file], cwd=cwd)
    return result.returncode == 0, result.stdout


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ok = True

    for example in EXAMPLES:
        py_path = os.path.join(base_dir, example)
        tex_name = os.path.splitext(example)[0] + '.tex'

        run_res = run([sys.executable, py_path], cwd=base_dir)
        if run_res.returncode != 0:
            ok = False
            print('[FAIL] generate {}\n{}'.format(example, run_res.stdout))
            continue

        tex_path = os.path.join(base_dir, tex_name)
        if not os.path.exists(tex_path):
            ok = False
            print('[FAIL] missing tex {}'.format(tex_name))
            continue

        print('[PASS] generated {}'.format(tex_name))
        compile_ok, compile_log = compile_tex(tex_name, base_dir)
        if compile_ok is None:
            print('[SKIP] {}'.format(compile_log))
        elif compile_ok:
            print('[PASS] compiled {}'.format(tex_name))
        else:
            ok = False
            print('[FAIL] compile {}\n{}'.format(tex_name, compile_log))

    if not ok:
        sys.exit(1)


if __name__ == '__main__':
    main()

