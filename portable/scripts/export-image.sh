#!/bin/bash
# Export the Docker image for embedding in portable builds
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT_DIR="${1:-$SCRIPT_DIR/../dist}"

echo "=== Exporting airbrowser image ==="

# Build the image first
echo "Building Docker image..."
cd "$ROOT_DIR"
docker build -t airbrowser:latest .

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Export image
echo "Exporting image to $OUTPUT_DIR/image.tar..."
docker save airbrowser:latest -o "$OUTPUT_DIR/image.tar"

# Compress it
echo "Compressing image..."
gzip -f "$OUTPUT_DIR/image.tar"

IMAGE_SIZE=$(du -h "$OUTPUT_DIR/image.tar.gz" | cut -f1)
echo "=== Image exported: $OUTPUT_DIR/image.tar.gz ($IMAGE_SIZE) ==="
