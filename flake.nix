{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in rec {

        python_env = pkgs.python3.withPackages (ps: with ps; [
          click
          numpy
          imageio
        ]);
    
        Packages.spectrum_painter = pkgs.python3.pkgs.buildPythonPackage rec {
          pname = "spectrum_painter";
          version = "0.1.0";
        
          src = ./.;
          doCheck = false;
        
          propagatedBuildInputs = [
            python_env
          ];
        };

        devShell = pkgs.mkShell { buildInputs = [ python_env ]; };
      });
}
