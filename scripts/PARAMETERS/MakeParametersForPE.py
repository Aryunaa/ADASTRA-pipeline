import json
import sys
import os.path

sys.path.insert(1, "/home/abramov/ASB-Project")
from scripts.HELPERS.paths import ploidy_dict_path, parallel_parameters_path
from scripts.HELPERS.helpers import read_synonims

out_path = parallel_parameters_path + 'PE_parameters.cfg'

cell_lines = ['K-562']#, 'MCF7', 'HCT-116']
test_names = [
    # "K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS357NWO_", it's too big
    "K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS603CUX_",
    "K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS906KIP_",
    "K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS389PVA_",
    "K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS392AAA_",
    "K562_myelogenous_leukemia!_labs_bradley-bernstein___biosamples_ENCBS639AAA_",
    "K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS577JGM_",
]
large = ['K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS352MRW_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS691VMX_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS994WPS_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS207UAM_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS125ACM_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS603CUX_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS357NWO_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS101QRF_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS320BUL_',
         'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS906KIP_'
         ]

small = [
    'K562_myelogenous_leukemia!_labs_sherman-weissman___biosamples_ENCBS039ENC_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS170SCN_',
    'K562_myelogenous_leukemia!_labs_vishwanath-iyer___biosamples_ENCBS775AAA_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS587AHU_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS534MHY_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS200VWP_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS352EMA_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS779EKH_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS789AAA_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS887FSB_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS957QHW_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS990OSB_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS788AAA_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS926CWO_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS302KJF_',
    'K562_myelogenous_leukemia!_labs_kevin-struhl___biosamples_ENCBS039ENC_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS913AGK_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS008URG_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS894HTX_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS742ILR_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS392SQX_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS778QBL_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS675IUA_',
    'K562_myelogenous_leukemia!GSE25416',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS765OBZ_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS818FPM_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS523ORN_',
    'K562_myelogenous_leukemia!_labs_bradley-bernstein___biosamples_ENCBS984VNR_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS706JJD_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS054WRH_',
    'K562_myelogenous_leukemia!GSE24685',
    'K562_myelogenous_leukemia!GSE28162',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS910CTC_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS164UBJ_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS559UBQ_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS277GLZ_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS026JDH_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS539IPB_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS579QSJ_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS962GKO_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS995QNX_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS852VOH_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS889YTW_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS145BAM_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS594GNK_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS967JDE_',
    'K562_myelogenous_leukemia!GSE24777',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS612SGW_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS422ZTW_',
    'K562_myelogenous_leukemia!_labs_peggy-farnham___biosamples_ENCBS038KVF_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS546RMD_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS770RPE_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS410RUZ_',
    'K562_myelogenous_leukemia!GSE30226',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS361MEX_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS250NTO_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS430OPI_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS241XDL_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS343LRB_',
    'K562_myelogenous_leukemia!GSE43579',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS739OBP_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS431ZXQ_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS340DSB_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS316CKF_',
    'K562_myelogenous_leukemia!GSE19545',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS109ENC_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS021UXC_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS670PDV_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS948PVM_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS488ZQI_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS401NIV_',
    'K562_myelogenous_leukemia!_labs_john-stamatoyannopoulos___biosamples_ENCBS511YCF_',
    'K562_myelogenous_leukemia!GSE26320',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS504MPM_',
    'K562_myelogenous_leukemia!GSE23730',
    'K562_myelogenous_leukemia!GSE70482',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS309IBB_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS848PQJ_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS094YFT_',
    'K562_myelogenous_leukemia!GSE50611',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS136FFT_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS660SLH_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS852AAA_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS983KMD_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS070CNU_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS027DJL_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS601AAA_',
    'K562_myelogenous_leukemia!_labs_john-stamatoyannopoulos___biosamples_ENCBS922RYG_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS861JYZ_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS405IFW_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS108KJU_',
    'K562_myelogenous_leukemia!GSE50610',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS638TGE_',
    'K562_myelogenous_leukemia!_labs_sherman-weissman___biosamples_ENCBS789AAA_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS283TEI_',
    'K562_myelogenous_leukemia!GSE26439',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS556OQY_',
    'K562_myelogenous_leukemia!GSE103445',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS789RGF_',
    'K562_myelogenous_leukemia!GSE107726',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS819JKS_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS051ABU_',
    'K562_myelogenous_leukemia!GSE70764',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS992FSA_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS602AAA_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS331LZB_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS846OZP_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS641AAS_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS903WFV_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS925NOW_',
    'K562_myelogenous_leukemia!GSE18868',
    'K562_myelogenous_leukemia!GSE19546',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS204XMM_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS353XCU_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS134NRZ_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS626KTH_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS156XSD_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS074NGX_',
    'K562_myelogenous_leukemia!_labs_peggy-farnham___biosamples_ENCBS667AAA_',
    'K562_myelogenous_leukemia!False',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS182OZC_',
    'K562_myelogenous_leukemia!GSE97661',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS609DLP_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS600AAA_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS383VKK_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS903THP_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS984PPX_',
    'K562_myelogenous_leukemia!_labs_sherman-weissman___biosamples_ENCBS787AAA_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS083LQN_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS231GMV_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS061XWL_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS889FGM_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS500RNP_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS364BHZ_',
    'K562_myelogenous_leukemia!GSE19235',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS142DQA_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS481LVE_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS667AAA_',
    'K562_myelogenous_leukemia!_labs_sherman-weissman___biosamples_ENCBS788AAA_',
    'K562_myelogenous_leukemia!_labs_bradley-bernstein___biosamples_ENCBS674MPN_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS271QIL_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS039TGQ_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS507YTF_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS544POC_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS757EXI_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS111WEH_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS828SMC_',
    'K562_myelogenous_leukemia!GSE92882',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS101CXP_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS559ERW_',
    'K562_myelogenous_leukemia!GSE29195',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS216ZMH_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS489ZOH_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS875VQC_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS246UOA_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS670LTO_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS852SOK_',
    'K562_myelogenous_leukemia!GSE70920',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS437BJN_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS039ENC_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS285PHZ_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS644RCS_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS426CWP_',
    'K562_myelogenous_leukemia!GSE32509',
    'K562_myelogenous_leukemia!GSE24632',
    'K562_myelogenous_leukemia!GSE19547',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS105RVN_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS716JYS_',
    'K562_myelogenous_leukemia!GSE55306',
    'K562_myelogenous_leukemia!_labs_peggy-farnham___biosamples_ENCBS175LWC_',
    'K562_myelogenous_leukemia!GSE39263',
    'K562_myelogenous_leukemia!GSE92879',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS661EXX_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS819AUE_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS105ZBV_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS851CNL_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS350VSG_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS577JGM_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS754HFN_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS091XYE_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS799VSJ_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS207FBE_',
    'K562_myelogenous_leukemia!GSE76145',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS237BHV_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS075MLD_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS996OLB_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS012WJD_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS542KXR_',
    'K562_myelogenous_leukemia!_labs_sherman-weissman___biosamples_ENCBS852AAA_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS903OXA_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS020CGZ_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS267LNH_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS082JCQ_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS936SUX_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS458HHF_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS808KRH_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS443JHG_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS733PPV_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS923ZGZ_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS075XHE_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS570ZDR_',
    'K562_myelogenous_leukemia!_labs_richard-myers___biosamples_ENCBS405DQO_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS557OXO_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS541VKI_',
    'K562_myelogenous_leukemia!_labs_michael-snyder___biosamples_ENCBS753IIO_',
    'K562_myelogenous_leukemia!_labs_kevin-white___biosamples_ENCBS885SBO_',
    'K562_myelogenous_leukemia!_labs_xiang-dong-fu___biosamples_ENCBS967ZYE_',
]

if __name__ == "__main__":
    with open(ploidy_dict_path, 'r') as read_file:
        d = json.loads(read_file.readline())
    cosmic_names, _ = read_synonims()
    keys = sorted(d.keys())
    with open(out_path, 'w') as file:
        for key in keys:
            name = key.split('!')[0]
            if key in large:
                continue
            if cosmic_names.get(name, '') not in cell_lines:
                continue
            is_empty = True
            for value in d[key]:
                if os.path.isfile(value):
                    is_empty = False
            if is_empty:
                continue
            file.write(key + '\n')
