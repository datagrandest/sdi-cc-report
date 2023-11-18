import sys

# from sdi_cc_report import (
#     sdi_cc_report_cli,
#     sdi_cc_report_eel,
#     sdi_cc_report_tk_cli,
#     sdi_cc_report_tk_gui,
#     sdi_cc_report_web,
# )

if __name__ == "__main__":
    # NOT IMPLEMENTED
    if len(sys.argv) == 2 and sys.argv[1] == "gui":
        # from sdi_cc_report import sdi_cc_report_tk_gui
        # sdi_cc_report_tk_gui.run()
        pass

    # NOT IMPLEMENTED
    elif len(sys.argv) == 2 and sys.argv[1] == "cli":
        # from sdi_cc_report import sdi_cc_report_tk_cli
        # sdi_cc_report_tk_cli.run()
        pass

    # NOT IMPLEMENTED
    elif len(sys.argv) > 1 and sys.argv[1] == "eel":
        # from sdi_cc_report import sdi_cc_report_eel
        # mode = sys.argv[2] if len(sys.argv) > 2 else 'prod'
        # sdi_cc_report_eel.run(mode)
        pass

    elif len(sys.argv) > 1 and sys.argv[1] == "web":
        from sdi_cc_report import sdi_cc_report_web

        mode = sys.argv[2] if len(sys.argv) > 2 else "prod"
        sdi_cc_report_web.run(mode)

    else:
        from sdi_cc_report import sdi_cc_report_cli

        sdi_cc_report_cli.run()
