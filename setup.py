from distutils.core import setup
import distutils
import py2exe
distutils.core.setup(
options = {
    "py2exe": {
        "dll_excludes": ["MSVCP90.dll"]
    }
}
)
setup(console=['nhentai.py'])
