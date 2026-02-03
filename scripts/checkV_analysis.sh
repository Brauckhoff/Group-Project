#!/usr/bin/env bash

# Check if the user provided an ID. If not, stop the script.
if [ -z "$1" ]; then
    echo "Error: You must provide an ID."
    echo "Usage: $0 <ID>"
    exit 1
fi

SAMPLE="$1"
ASSEMBLER="$2"

pre="/teachstor/share/groupprojectWS25/groupC"
INPUT_DIR="viralverify/${ASSEMBLER}/${SAMPLE}_${ASSEMBLER}"
OUT_DIR="checkV/${ASSEMBLER}/${SAMPLE}"


# Create output directories
mkdir -p "${OUT_DIR}"

echo "[INFO] Processing sample: ${SAMPLE}"

# Extract viral contigs
COMBINED_VIRAL_FASTA="${OUT_DIR}/${SAMPLE}_all_viral_contigs.fasta"
cat "${INPUT_DIR}"/*/*_virus.fasta > "${COMBINED_VIRAL_FASTA}" 2>/dev/null

# Run CheckV
echo "[INFO] Running CheckV"

checkv end_to_end \
  "${COMBINED_VIRAL_FASTA}" \
  "${OUT_DIR}/results" \
  -d "/teachstor/share/groupprojectWS25/groupC/references/checkv_db/checkv-db-v1.5/" \
  -t 16

echo "[INFO] Done for sample: ${SAMPLE}"