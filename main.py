import ansa,logging,sys
import buconnect,bumesh,helpers,bubase,plugs




if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    rail_path = r'asset/4m-model.key'
    spacer_path =r'asset/spacer.key'
    rail = plugs.Eve(rail_path)
    spacer = plugs.Eve(spacer_path)

    logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    hdl = logging.StreamHandler()

    hdl.setStream(sys.stdout)
    hdl.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    hdl.setFormatter(formatter)

    logging.debug('duh')
   
    # duh = rail._parse_css_name()
    print(rail.mcss)

    #-----------------------------------
    time.end()