{ pkgs ? import <nixos-unstable> {}}:
  pkgs.mkShell {
    nativeBuildInputs = let
      env = pyPkgs : with pyPkgs; [
        # default
        decorator
        numpy
        scipy
        matplotlib
        pandas
        ipython

        # test
        pytest
        pytest-cov
        codecov
        black
        memory_profiler
      ];
    in with pkgs; [
      (python39.withPackages env)
    ];
}

