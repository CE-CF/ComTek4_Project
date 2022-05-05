{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "esp-idf-env";

  buildInputs = with pkgs; [
    (pkgs.callPackage ./esp32-toolchain.nix {})

    git
    wget
    gnumake

    flex
    bison
    gperf
    pkgconfig

    cmake

    ncurses5

    ninja

    (python3.withPackages (p: with p; [
      pip
      virtualenv
    ]))
  ];

  shellHook = ''
    export IDF_PATH=$(pwd)/esp-idf
    export PATH=$IDF_PATH/tools:$PATH
    export IDF_PYTHON_ENV_PATH=$(pwd)/.python_env

    if [ ! -e $IDF_PYTHON_ENV_PATH ]; then
      python -m venv $IDF_PYTHON_ENV_PATH
      . $IDF_PYTHON_ENV_PATH/bin/activate
      pip install -r $IDF_PATH/requirements.txt
    else
      . $IDF_PYTHON_ENV_PATH/bin/activate
    fi
  '';
}
