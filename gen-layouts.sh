#!/usr/bin/env sh

OUT_DIR="rand-layouts"
METHODS="dfs kruskal prim"
PROBLEM_TYPES="search corners food"

if [ ! -d "${OUT_DIR}" ]; then
    mkdir -p "${OUT_DIR}"
fi

for method in ${METHODS}; do
    for ptype in ${PROBLEM_TYPES}; do
        for size in `seq 10 5 30`; do
            for cprob in `seq 0.1 0.1 0.4`; do
                for seed in `seq 0 1 5`; do
                    out_file="${OUT_DIR}/${method}_${size}_${cprob}_${seed}_${ptype}.lay"
                    python3 -m pacman_mapgen \
                        --method "${method}" \
                        --problem-type ${ptype} \
                        --width ${size} \
                        --height ${size} \
                        --cycle-probability ${cprob} \
                        --seed ${seed} > "${out_file}"
                done
            done
        done
    done
done
