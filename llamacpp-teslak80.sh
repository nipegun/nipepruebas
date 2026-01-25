#!/bin/bash

    # Crear carpeta de Git
      mkdir -p $HOME/Git/ 2> /dev/null

    # Clonar Git
      cd $HOME/Git/
      # Borrar versión ya instalada
        rm -rf $HOME/Git/llama.cpp/
      git clone --depth 1 https://github.com/ggerganov/llama.cpp.git

    # Instalar dependencias para compilar
      sudo apt-get -y update
      sudo apt-get -y install cmake
      sudo apt-get -y install build-essential
      sudo apt-get -y install libcurl4-openssl-dev
      sudo apt-get -y install ccache
      sudo apt-get -y install libncurses-dev

mkdir -p $HOME/Git/llama.cpp/build
cd $HOME/Git/llama.cpp/build
cmake ..                      \
  -DGGML_CUDA=ON              \
  -DGGML_CUDA_FORCE=ON        \
  -DGGML_CUDA_ARCHS=37        \
  -DGGML_CUDA_F16=OFF         \
  -DGGML_CUDA_NO_PEER_COPY=ON \
  -DGGML_NATIVE=OFF           \
  -DCMAKE_CXX_FLAGS="-march=ivybridge -mtune=ivybridge -O3"

cmake --build . --config Release -- -j$(nproc)







CUDA_VISIBLE_DEVICES=0 \
$HOME/IA/LlamaCPP/llama-cli \
  -m modelo.gguf \
  -ngl 20 \
  --stats

