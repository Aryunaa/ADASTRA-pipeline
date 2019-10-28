import sys
from typing import List, Union

sys.path.insert(1, "/home/abramov/ASB-Project")
from scripts.HELPERS.paths import make_black_list, create_path_from_GTRD_function, GTRD_slice_path, \
    create_line_for_snp_calling

callers_names = ['macs', 'sissrs', 'cpics', 'gem']

chr_l = [248956422, 242193529, 198295559, 190214555, 181538259, 170805979, 159345973,
         145138636, 138394717, 133797422, 135086622, 133275309, 114364328, 107043718,
         101991189, 90338345, 83257441, 80373285, 58617616, 64444167, 46709983, 50818468,
         156040895, 57227415]

Nucleotides = {'A', 'T', 'G', 'C'}


class ChromPos:
    chrs = dict(zip(['chr' + str(i) for i in range(1, 23)] + ['chrX', 'chrY'], chr_l))

    def __init__(self, chr, pos):
        if chr not in self.chrs:
            raise ValueError("Not in valid chromosomes {}".format(chr))
        self.chr = chr
        self.pos = int(pos)

    def __lt__(self, other):
        if self.chr == other.chr:
            return self.pos < other.pos
        else:
            return self.chr < other.chr

    def __gt__(self, other):
        if self.chr == other.chr:
            return self.pos > other.pos
        else:
            return self.chr > other.chr

    def __le__(self, other):
        if self.chr == other.chr:
            return self.pos <= other.pos
        else:
            return self.chr <= other.chr

    def __ge__(self, other):
        if self.chr == other.chr:
            return self.pos >= other.pos
        else:
            return self.chr >= other.chr

    def __eq__(self, other):
        return (self.chr, self.pos) == (other.chr, other.pos)

    def __ne__(self, other):
        return (self.chr, self.pos) != (other.chr, other.pos)

    def distance(self, other):
        if self.chr != other.chr:
            return float('inf')
        return abs(self.pos - other.pos)


def unpack_segments(line):
    if isinstance(line, (list, tuple)):
        return line
    if line[0] == '#':
        return []
    return line.strip().split('\t')


class Intersection:
    def __init__(self, snps, segments, write_segment_args=False, write_intersect=False,
                 unpack_segments_function=unpack_segments, unpack_snp_function=lambda x: x):
        self.snps = iter(snps)
        self.segments = iter(segments)
        self.unpack_snp_function = unpack_snp_function
        self.unpack_segments_function = unpack_segments_function
        self.write_segment_args = write_segment_args
        self.write_intersect = write_intersect
        self.snp_args = []
        self.seg_args = []
        self.snp_coordinate = None
        self.segment_start = None
        self.segment_end = None
        self.has_segments = True

    def __iter__(self):
        return self

    def return_snp(self, intersect):
        return [self.snp_coordinate.chr, self.snp_coordinate.pos] + self.snp_args \
               + [int(intersect)] * self.write_intersect \
               + [arg * intersect for arg in self.seg_args] * self.write_segment_args

    def get_next_snp(self):
        try:
            snp_chr, pos, *self.snp_args = self.unpack_snp_function(next(self.snps))
            self.snp_coordinate = ChromPos(snp_chr, pos)
        except ValueError:
            self.get_next_snp()

    def get_next_segment(self):
        try:
            seg_chr, start_pos, end_pos, *self.seg_args = self.unpack_segments_function(next(self.segments))

            self.segment_start = ChromPos(seg_chr, start_pos)
            self.segment_end = ChromPos(seg_chr, end_pos)
        except StopIteration:
            self.has_segments = False
        except ValueError:
            self.get_next_segment()

    def __next__(self):
        if self.snp_coordinate is None:
            self.get_next_snp()
        if self.segment_start is None:
            self.get_next_segment()

        while self.has_segments and self.snp_coordinate >= self.segment_end:
            self.get_next_segment()

        if self.has_segments and self.snp_coordinate >= self.segment_start:
            x = self.return_snp(True)
            self.get_next_snp()
            return x
        else:
            x = self.return_snp(False)
            self.get_next_snp()
            return x


def make_dict_from_vcf(vcf, vcf_dict):
    for line in vcf:
        if line[0] == '#':
            continue
        line = line.split()
        chr = line[0]
        if chr not in ChromPos.chrs:
            raise ValueError('{} not in valid chrs'.format(chr))
        pos = int(line[1])
        if not len(line[3]) == 1 or not len(line[4]) == 1:
            continue
        if line[3] not in Nucleotides or line[4] not in Nucleotides:
            continue
        Inf = line[-1].split(':')
        R = int(Inf[1].split(',')[0])
        if Inf[1].split(",")[1] == "":
            print(line)
            print(vcf)
        A = int(Inf[1].split(',')[1])
        if min(R, A) < 3:
            continue
        GT = Inf[0]
        if GT != '0/1':
            continue
        ID = line[2]
        REF = line[3]
        ALT = line[4]
        try:
            prev_value = vcf_dict[(chr, pos, ID, REF, ALT)]
            vcf_dict[(chr, pos, ID, REF, ALT)] = (R + prev_value[0], A + prev_value[1])
        except KeyError:
            vcf_dict[(chr, pos, ID, REF, ALT)] = (R, A)


def unpack(line, use_in):
    line_split = line.strip().split('\t')
    chr = line_split[0]
    pos = int(line_split[1])
    ID = line_split[2]
    ref = line_split[3]
    alt = line_split[4]
    ref_c, alt_c = map(int, line_split[5:7])
    if use_in == "PloidyEstimation":
        return chr, pos, ID, ref, alt, ref_c, alt_c
    repeat = line_split[7]
    difference = len(callers_names)
    peaks = map(int, line_split[8:8 + difference])
    in_callers = dict(zip(callers_names, [peaks]))
    if use_in == "Pcounter":
        if line[0] == '#':
            return []
        else:
            return chr, pos, ID, ref, alt, ref_c, alt_c, repeat, in_callers

    ploidy = float(line_split[8 + difference])
    dip_qual, lq, rq, seg_c = map(int, line_split[9 + difference:13 + difference])

    if line_split[13 + difference] == '.':
        p_ref = '.'
        p_alt = '.'
    else:
        p_ref, p_alt = map(float, line_split[13 + difference:15 + difference])
    if use_in == "Aggregation":
        return chr, pos, ID, ref, alt, ref_c, alt_c, repeat, in_callers, ploidy, dip_qual, lq, rq, seg_c, p_ref, p_alt

    raise ValueError('{} not in Aggregation, Pcounter, PloidyEstimation options for function usage'.format(use_in))


def pack(values):
    return '\t'.join(map(str, values)) + '\n'


def make_list_for_VCFs(out_path, condition_function):  # condition function must takes path and return boolean
    black_list = make_black_list()
    counted_controls = set()

    with open(GTRD_slice_path, "r") as master_list, open(out_path, "w") as out:
        for line in master_list:
            if line[0] == "#":
                continue
            split_line = line.strip().split("\t")
            if split_line[0] not in black_list:
                vcf_path = create_path_from_GTRD_function(split_line, for_what="vcf")
                if condition_function(vcf_path):
                    out.write(create_line_for_snp_calling(split_line))
            if len(split_line) > 10 and split_line[10] not in black_list:
                vcf_path = create_path_from_GTRD_function(split_line, for_what="vcf", ctrl=True)
                if vcf_path in counted_controls:
                    continue
                counted_controls.add(vcf_path)
                if condition_function(vcf_path):
                    out.write(create_line_for_snp_calling(split_line, is_ctrl=True))


class Reader:
    CGH_path = ''
    SNP_path = ''
    Cosmic_path = ''
    synonims_path = ''
    
    def read_Cosmic(self, name, mode='normal'):
        with open(self.Cosmic_path, 'r') as file:
            result = []
            for line in file:
                if line[0] == '#':
                    continue
                line = line.strip().split(',')
                # if int(line[4]) in {4,6,8} or line[3] == '0': continue
                if line[0] != name:
                    continue
                if 'chr' + line[4] not in ChromPos.chrs:
                    continue
                if int(line[10]) == 0:
                    continue
                
                if mode == 'normal':
                    value = int(line[11]) / int(line[10]) - 1
                elif mode == 'total':
                    value = int(line[11])
                else:
                    raise ValueError(mode)
                
                result.append(['chr' + line[4], int(line[5]), int(line[6]), value])
            if not result:
                raise KeyError(name)
            # result.sort_items()
            return result
    
    def read_SNPs(self, method='normal'):
        with open(self.SNP_path, 'r') as file:
            result = []
            uniq_segments_count = 0
            previous_segment = []
            for line in file:
                if line[0] == '#':
                    split_header = line[1:].split('!')
                    datasets_number = split_header[0]
                    lab = split_header[1]
                    aligns = split_header[2]
                    if aligns:
                        aligns = ','.join(aligns.split('>'))
                    else:
                        aligns = ''
                    continue
                line = line.strip().split("\t")
                if line[0] not in ChromPos.chrs:
                    continue
                current_segment = [float(line[4]), int(line[5]), int(line[6])]
                if previous_segment != current_segment:
                    uniq_segments_count += 1
                    previous_segment = current_segment
                if method == 'normal':
                    if line[4] == 0:
                        continue
                    result.append([line[0], int(line[1])] + current_segment)
                elif method == 'naive':
                    ref = int(line[2])
                    alt = int(line[3])
                    if min(ref, alt) == 0:
                        continue
                    result.append([line[0], int(line[1]), max(ref, alt) / min(ref, alt) - 1, 10000, 10000])
                else:
                    raise KeyError(method)

            return datasets_number, lab, result, aligns, uniq_segments_count
    
    def read_CGH(self, cgh_name):
        cgnames = ['BR:MCF7', 'BR:MDA-MB-231', 'BR:HS 578T', 'BR:BT-549', 'BR:T-47D', 'CNS:SF-268', 'CNS:SF-295',
                   'CNS:SF-539', 'CNS:SNB-19', 'CNS:SNB-75', 'CNS:U251', 'CO:COLO 205', 'CO:HCC-2998', 'CO:HCT-116',
                   'CO:HCT-15', 'CO:HT29', 'CO:KM12', 'CO:SW-620', 'LE:CCRF-CEM', 'LE:HL-60(TB)', 'LE:K-562',
                   'LE:MOLT-4', 'LE:RPMI-8226', 'LE:SR', 'ME:LOX IMVI', 'ME:MALME-3M', 'ME:M14', 'ME:SK-MEL-2',
                   'ME:SK-MEL-28', 'ME:SK-MEL-5', 'ME:UACC-257', 'ME:UACC-62', 'ME:MDA-MB-435', 'ME:MDA-N',
                   'LC:A549/ATCC', 'LC:EKVX', 'LC:HOP-62', 'LC:HOP-92', 'LC:NCI-H226', 'LC:NCI-H23', 'LC:NCI-H322M',
                   'LC:NCI-H460', 'LC:NCI-H522', 'OV:IGROV1', 'OV:OVCAR-3', 'OV:OVCAR-4', 'OV:OVCAR-5', 'OV:OVCAR-8',
                   'OV:SK-OV-3', 'OV:NCI/ADR-RES', 'PR:PC-3', 'PR:DU-145', 'RE:786-0', 'RE:A498', 'RE:ACHN',
                   'RE:CAKI-1', 'RE:RXF 393', 'RE:SN12C', 'RE:TK-10', 'RE:UO-31']
        idx = cgnames.index(cgh_name) + 3
        N = 0
        with open(self.CGH_path, 'r') as file:
            result = []
            for line in file:
                line = line.strip().split('\t')
                chr = line[0]
                if chr not in ChromPos.chrs:
                    continue
                pos = (int(line[1]) + int(line[2])) // 2
                try:
                    value = 2 ** (1 + float(line[idx]))
                except ValueError:
                    continue
                N += 1
                result.append([chr, pos, value, 100, 100])
            # result.sort_items()
            return N, result
    
    def read_synonims(self):
        cosmic_names = dict()
        cgh_names = dict()
        with open(self.synonims_path, 'r') as file:
            for line in file:
                line = line.strip('\n').split('\t')
                if line[1] and line[2]:
                    name = line[0].replace(')', '').replace('(', '').replace(' ', '_')
                    cosmic_names[name] = line[1]
                    cgh_names[name] = line[2]
        return cosmic_names, cgh_names
