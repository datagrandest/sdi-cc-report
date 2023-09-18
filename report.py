import sys

# from master import master_tk_gui, master_tk_cli, master_cli, master_eel, master_web

if __name__ == "__main__":
    
    # NOT IMPLEMENTED
    if len(sys.argv) == 2 and sys.argv[1] == 'gui':
        # from master import master_tk_gui
        # master_tk_gui.run()
        pass
    
    # NOT IMPLEMENTED
    elif len(sys.argv) == 2 and sys.argv[1] == 'cli':
        # from master import master_tk_cli
        # master_tk_cli.run()
        pass
    
    # NOT IMPLEMENTED
    elif len(sys.argv) > 1 and sys.argv[1] == 'eel':
        # from master import master_eel
        # mode = sys.argv[2] if len(sys.argv) > 2 else 'prod'
        # master_eel.run(mode)
        pass
    
    # NOT IMPLEMENTED
    elif len(sys.argv) > 1 and sys.argv[1] == 'web':
        # from master import master_web
        # mode = sys.argv[2] if len(sys.argv) > 2 else 'gui'
        # master_web.run(mode)
        pass
        
    else:
        from sdi_cc_report import sdi_cc_report_cli
        sdi_cc_report_cli.run()