import gzip
import bz2
import lzma
import zlib
import os

# Test di compressione e decompressione su vari algoritmi

def test_compression_algorithms():
    data = b"SuperAgent compression test: dati di esempio molto ripetuti! " * 1000
    results = {}
    files = []

    # gzip
    gzip_file = "test_gzip.gz"
    with gzip.open(gzip_file, "wb") as f:
        f.write(data)
    with gzip.open(gzip_file, "rb") as f:
        decompressed = f.read()
    results['gzip'] = (len(data), os.path.getsize(gzip_file), decompressed == data)
    files.append(gzip_file)

    # bz2
    bz2_file = "test_bz2.bz2"
    with bz2.open(bz2_file, "wb") as f:
        f.write(data)
    with bz2.open(bz2_file, "rb") as f:
        decompressed = f.read()
    results['bz2'] = (len(data), os.path.getsize(bz2_file), decompressed == data)
    files.append(bz2_file)

    # lzma
    lzma_file = "test_lzma.xz"
    with lzma.open(lzma_file, "wb") as f:
        f.write(data)
    with lzma.open(lzma_file, "rb") as f:
        decompressed = f.read()
    results['lzma'] = (len(data), os.path.getsize(lzma_file), decompressed == data)
    files.append(lzma_file)

    # zlib (in-memory)
    compressed = zlib.compress(data)
    decompressed = zlib.decompress(compressed)
    results['zlib'] = (len(data), len(compressed), decompressed == data)

    # Pulizia file
    for f in files:
        try:
            os.remove(f)
        except Exception:
            pass

    print("--- Risultati test compressione ---")
    for algo, (orig_size, comp_size, ok) in results.items():
        print(f"{algo}: originale={orig_size}, compresso={comp_size}, integrità={'OK' if ok else 'ERRORE'}")

if __name__ == "__main__":
    test_compression_algorithms()
