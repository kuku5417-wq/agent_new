"""사내망 동료용 배포 zip 만들기.

사용 (이 폴더에서):
    python -X utf8 make_bundle.py                         옆 폴더 "agent 가이드"(shi_dev)의 지금 커밋으로
    python -X utf8 make_bundle.py --shi <shi_dev 폴더> --ref v0.4.0   정한 태그·커밋으로

결과: dist/shi_사내망_<버전>.zip
  ├── 설치_안내.md          동료용 (이 폴더의 것 — shi_dev 것을 덮는다)
  ├── 시작_한장.md, 자주_쓰는_말.md, 자주_묻는_것.md
  ├── 사내망_적용.md        shi_dev docs 에서 (기존 앱을 다시 지을 때)
  ├── install_local.py      shi_dev 에서
  ├── plugins/shi/…         shi_dev 에서 (에이전트·스킬·훅·틀)
  ├── .claude-plugin/marketplace.json   (로컬 폴더 마켓플레이스로도 설치 가능)
  └── VERSION               shi 판, 만든 날, 출처 커밋
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUR_DOCS = ["설치_안내.md", "시작_한장.md", "자주_쓰는_말.md", "자주_묻는_것.md"]
FROM_SHI = ["install_local.py", ".claude-plugin/marketplace.json"]
FROM_SHI_DIRS = ["plugins/shi"]
FROM_SHI_RENAME = {"docs/사내망_적용.md": "사내망_적용.md"}
SKIP = {"__pycache__", ".DS_Store"}


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def shi_files(repo: Path, ref: str | None) -> tuple[dict[str, bytes], str]:
    """shi_dev 에서 필요한 파일을 {경로: 내용} 으로. ref 가 있으면 그 커밋에서, 없으면 지금 작업 폴더에서."""
    files: dict[str, bytes] = {}
    if ref:
        names = git(repo, "-c", "core.quotepath=false", "ls-tree", "-r", "--name-only", ref).decode("utf-8").splitlines()
        for n in names:
            if n in FROM_SHI or n in FROM_SHI_RENAME or any(n.startswith(d + "/") for d in FROM_SHI_DIRS):
                files[n] = git(repo, "show", f"{ref}:{n}")
        commit = git(repo, "rev-parse", "--short", ref).decode().strip()
    else:
        for n in FROM_SHI + list(FROM_SHI_RENAME):
            p = repo / n
            if p.exists():
                files[n] = p.read_bytes()
        for d in FROM_SHI_DIRS:
            for p in sorted((repo / d).rglob("*")):
                if p.is_file() and not SKIP & set(p.parts):
                    files[p.relative_to(repo).as_posix()] = p.read_bytes()
        try:
            commit = git(repo, "rev-parse", "--short", "HEAD").decode().strip()
            if git(repo, "status", "--porcelain").strip():
                commit += "+고친것있음"
        except (OSError, subprocess.CalledProcessError):
            commit = "git 아님"
    return files, commit


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="사내망 동료용 shi 배포 zip")
    ap.add_argument("--shi", default=str(HERE.parent / "agent 가이드"), help="shi_dev 저장소 폴더")
    ap.add_argument("--ref", help="태그나 커밋 (없으면 작업 폴더 그대로)")
    a = ap.parse_args()
    repo = Path(a.shi).resolve()
    if not (repo / "plugins" / "shi").is_dir():
        print(f"shi_dev 폴더가 아니다: {repo}", file=sys.stderr)
        return 1
    files, commit = shi_files(repo, a.ref)
    missing = [n for n in FROM_SHI + list(FROM_SHI_RENAME) if n not in files]
    if missing or "plugins/shi/.claude-plugin/plugin.json" not in files:
        print(f"shi_dev 에 없는 파일: {missing}", file=sys.stderr)
        return 1
    version = json.loads(files["plugins/shi/.claude-plugin/plugin.json"])["version"]
    for d in OUR_DOCS:
        if not (HERE / d).exists():
            print(f"이 폴더에 없는 문서: {d}", file=sys.stderr)
            return 1

    out = HERE / "dist" / f"shi_사내망_{version}.zip"
    out.parent.mkdir(exist_ok=True)
    root = f"shi_사내망_{version}/"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in sorted(files.items()):
            z.writestr(root + FROM_SHI_RENAME.get(n, n), data)
        for d in OUR_DOCS:
            z.writestr(root + d, (HERE / d).read_bytes())  # shi_dev 의 설치_안내.md 를 동료용으로 덮는다
        z.writestr(root + "VERSION", f"shi {version}\n만든 날 {time.strftime('%Y-%m-%d %H:%M')}\n출처 shi_dev {commit}\n")
    out.write_bytes(buf.getvalue())

    names = zipfile.ZipFile(out).namelist()
    print(f"만듦: {out}  ({out.stat().st_size // 1024} KB, 파일 {len(names)}개)")
    print(f"shi {version} / 출처 {commit}")
    print("다음: NAS 배포\\shi\\v" + version + "\\ 에 복사 (사람) → 안내 페이지의 경로·판 갱신")
    return 0


if __name__ == "__main__":
    sys.exit(main())
