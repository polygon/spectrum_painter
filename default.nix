{ sources ? import ./nix/sources.nix
, pkgs ? import sources.nixpkgs {}
}:
with pkgs; 
let
  python3-with-deps = python3.withPackages (ps: with ps; [
    click
    numpy
    imageio
  ]);
in
python3.pkgs.buildPythonPackage rec {
  pname = "spectrum_painter";
  version = "0.1.0";

  src = ./.;
  doCheck = false;
  
  buildInputs = [
    python3-with-deps
  ];
}
