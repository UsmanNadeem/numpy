from __future__ import division, absolute_import, print_function               

from distutils.unixccompiler import UnixCCompiler                              

class LLVMCCompiler(UnixCCompiler):

    """
    LLVM clang compiler.
    """

    compiler_type = 'llvm'
    cc_exe = 'clang'
    cxx_exe = 'clang++'

    def __init__(self, verbose=0, dry_run=0, force=0):
        UnixCCompiler.__init__(self, verbose, dry_run, force)
        cc_compiler = self.cc_exe
        cxx_compiler = self.cxx_exe
        self.set_executables(compiler=cc_compiler +
                                      ' -O3 -fPIC -Wno-implicit-function-declaration -Wno-implicit-int',
                             compiler_so=cc_compiler +
                                         ' -O3 -fPIC -Wno-implicit-function-declaration -Wno-implicit-int',
                             compiler_cxx=cxx_compiler +
                                          ' -O3 -fPIC -Wno-implicit-function-declaration -Wno-implicit-int',
                             linker_exe=cc_compiler,
                             linker_so=cc_compiler +
                                       ' -shared')
