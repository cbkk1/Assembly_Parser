import re
import chardet

def detect_encoding(file_path):
    """Detect the encoding of a file to prevent UnicodeDecodeError."""
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read(100000))  # Read first 100KB for detection
        return result["encoding"]

def parse_assembly_file(file_path):
    """Parses an assembly file to count occurrences of different addressing modes."""
    mode_counts = {
        "Memory Indirect": 0,
        "Scaled Indexed": 0,
        "Register Indirect": 0,
        "Immediate": 0,
        "Displacement": 0
    }

    # Regex patterns for different addressing modes
    patterns = {
        "Memory Indirect": re.compile(r"\[\s*\[[a-zA-Z0-9%_]+\]\s*\]"),
        "Scaled Indexed": re.compile(r"\[\s*([a-zA-Z0-9%_]+)\s*\+\s*([a-zA-Z0-9%_]+)\s*\*\s*(\d+)\s*\]"),
        "Register Indirect": re.compile(r"\[\s*([a-zA-Z0-9%_]+)\s*\]"),
        "Immediate": re.compile(r"(?<![\w\]])(?:0x[0-9A-Fa-f]+|\b\d+\b)(?![\w\]])"),
        "Displacement": re.compile(r"\[\s*([a-zA-Z0-9%_]+)\s*\+\s*(0x[0-9A-Fa-f]+|\d+)\s*\]")
    }

    # Detect encoding
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")

    with open(file_path, "r", encoding=encoding, errors="ignore") as file:
        for line in file:
            for mode, pattern in patterns.items():
                if pattern.search(line):
                    mode_counts[mode] += 1

    return mode_counts

# Run the parser and print the results
file_path = "assemble.txt"
mode_counts = parse_assembly_file(file_path)

print("\nAddressing Mode Counts:")
for mode, count in mode_counts.items():
    print(f"{mode}: {count}")

