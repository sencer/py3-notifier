from distutils.core import setup

setup(
    name="py3notifier",
    version="0.1",
    description="py3status module for i3-notifier",
    author="Sencer Selcuk",
    packages=["py3notifier"],
    entry_points={"py3status": ["module = py3notifier.notifications"]},
)
