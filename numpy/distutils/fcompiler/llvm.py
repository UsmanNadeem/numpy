from __future__ import division, absolute_import, print_function
                                                                               
import sys                                                                     
                                                                               
from numpy.distutils.fcompiler import FCompiler, dummy_fortran_file
from sys import platform                                                       
from os.path import join, dirname, normpath

compilers = ['LLVMFlangCompiler']

import functools

class LLVMFlangCompiler(FCompiler):
    compiler_type = 'llvm'
    description = 'LLVM Flang Compiler'
    version_pattern = r'\s*flang.*version (?P<version>[\d.-]+).*'

    ar_exe = 'lib.exe'
    exe_path='/prj/llvm-arm/home/mnadeem/llvm/install_community_mainline_tip/bin/flang-new'
    possible_executables = ['flang-new']

    executables = {
        'version_cmd': ["flang-new", "--version"],
        'compiler_f77': ["flang-new", "-fPIC"],
        'compiler_fix': ["flang-new", "-fPIC", "-ffixed-form"],
        'compiler_f90': ["flang-new", "-fPIC"],
        'linker_so': ["flang-new", "-fPIC", "-shared", "-flang-experimental-exec"],
        'archiver': ["ar", "-cr"],
        'ranlib':  None
    }

    pic_flags = ["-fPIC", "-DPIC"]
    c_compiler = 'clang'
    module_dir_switch = '-module-dir '  # Don't remove ending space!

    def get_libraries(self):
        opt = FCompiler.get_libraries(self)
        opt.extend(['pgmath', 'gfortran' , 'Fortran_main' , 'FortranRuntime' , 'FortranDecimal'])
        return opt

    @functools.lru_cache(maxsize=128)
    def get_library_dirs(self):
        """List of compiler library directories."""
        opt = FCompiler.get_library_dirs(self)
        flang_dir = dirname(self.executables['compiler_f77'][0])
        opt.append(normpath(join(flang_dir, '..', 'lib')))

        return opt

    def get_flags(self):
        return []

    def get_flags_free(self):
        return []

    def get_flags_debug(self):
        return ['-g']

    def get_flags_opt(self):
        return ['-O3']

    def get_flags_arch(self):
        return []

    def runtime_library_dir_option(self, dir):
        return '-Wl,-rpath=%s' % dir


if __name__ == '__main__':
    from distutils import log
    log.set_verbosity(2)
    from numpy.distutils import customized_fcompiler
    print(customized_fcompiler(compiler="llvm").get_version())

