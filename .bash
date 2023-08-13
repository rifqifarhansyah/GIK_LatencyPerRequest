#!/bin/bash
set -e

sudo apt-get update
echo "Y" | sudo apt-get upgrade
git clone https://github.com/microsoft/DiskANN.git
cd DiskANN/
sudo apt install make cmake g++ libaio-dev libgoogle-perftools-dev clang-format libboost-all-dev
echo "Y"
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18487/l_BaseKit_p_2022.1.2.146.sh
sudo sh l_BaseKit_p_2022.1.2.146.sh -a --components intel.oneapi.lin.mkl.devel --action install --eula accept -s
echo "Y"
mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j
mkdir -p data && cd data/
wget ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
tar -xf sift.tar.gz
cd ..
./apps/utils/fvecs_to_bin float data/sift/sift_learn.fvecs data/sift/sift_learn.fbin
./apps/utils/fvecs_to_bin float data/sift/sift_query.fvecs data/sift/sift_query.fbin
./apps/utils/compute_groundtruth --data_type float --dist_fn l2 --base_file data/sift/sift_learn.fbin --query_file data/sift/sift_query.fbin --gt_file data/sift/sift_query_learn_gt100 --K 100
./apps/build_disk_index --data_type float --dist_fn l2 --data_path data/sift/sift_learn.fbin --index_path_prefix data/sift/disk_index_sift_learn_R32_L50_A1.2 -R 32 -L50 -B 0.003 -M 1
./apps/search_disk_index --data_type float --dist_fn l2 --index_path_prefix data/sift/disk_index_sift_learn_R32_L50_A1.2 --query_file data/sift/sift_query.fbin --gt_file data/sift/sift_query_learn_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res --num_nodes_to_cache 10000 -T 8

# setting untuk jalankan server
sudo apt install libcpprest-dev
cmake -DRESTAPI=True -DCMAKE_BUILD_TYPE=Release ..
make -j
./apps/restapi/ssd_server --address http://localhost:3000/ --data_type float --index_path_prefix data/sift/disk_index_sift_learn_R32_L50_A1.2  --num_nodes_to_cache 10000 --num_threads 8
