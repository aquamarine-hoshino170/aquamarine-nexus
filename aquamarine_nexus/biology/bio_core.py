class NexusBioSeq:
    """Bio-Molecular Sequence & Bioinformatics Engine (Biopython Alternative)"""
    GENETIC_CODE = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }

    AA_MASS = {
        'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.16,
        'E': 147.13, 'Q': 146.15, 'G': 75.07,  'H': 155.16, 'I': 131.18,
        'L': 131.18, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
        'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
    }

    @staticmethod
    def reverse_complement(dna_seq: str) -> str:
        comp_map = str.maketrans("ATGCUatgcu", "TACGAtacga")
        return dna_seq.translate(comp_map)[::-1].upper()

    @staticmethod
    def transcribe(dna_seq: str) -> str:
        """DNA to mRNA transcription (T -> U)"""
        return dna_seq.upper().replace('T', 'U')

    @staticmethod
    def translate(dna_seq: str) -> dict:
        """Translates DNA sequence into Amino Acid Polypeptide Chain"""
        seq = dna_seq.upper()
        protein = []
        for i in range(0, len(seq) - 2, 3):
            codon = seq[i:i+3]
            aa = NexusBioSeq.GENETIC_CODE.get(codon, '?')
            if aa == '_': # Stop Codon
                protein.append("*")
                break
            protein.append(aa)
        poly = "".join(protein)
        
        # Molecular Weight Calculation
        mw = sum(NexusBioSeq.AA_MASS.get(aa, 0.0) for aa in poly if aa != '*')
        if len(poly) > 1:
            mw -= (len(poly) - 1) * 18.015 # Remove water from peptide bonds
        return {"peptide_chain": poly, "amino_acids_count": len(poly), "molecular_weight_Da": round(mw, 2)}
