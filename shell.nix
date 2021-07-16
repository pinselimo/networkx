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

        # test
        pytest
        pytest-cov
        codecov
        black
      ];
    in with pkgs; [
      (python39.withPackages env)
    ];
}

