let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.matplotlib
      python-pkgs.pytorch
      python-pkgs.torchvision
      python-pkgs.onnx
      python-pkgs.onnxruntime
    ]))
    protobuf
  ];
}
