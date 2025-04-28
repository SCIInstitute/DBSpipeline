"""
implantation profiles house the geometric settings of the implanted devices for a specific patient.  This script is an example of how these profiles should be set up
"""

import os


implantation = {}

implantation["subject"] = "example"
# configuration
#   two lead, four lead
#   single IPG, double IPG
#   two strips,

geom_dir = "SCIRun_files/ImplantGeoms"

implantation["configuration"] = {"IPG": "twoIPG",
                                  "depthLead" : "fourLead",
                                  "stripElectrodes": "twoStrips"}
implantation["geom_dir"] = geom_dir

implantation["IPG"] = {
            "name" : ( "Left" , "Right"),
            "filename": ( "IPG_left_plan.stl", "IPG_right_plan.stl" )
}


implantation["depthLead"] = {}
implantation["depthLead"]["name"] = ("Left GPi", "Left CM", "Right GPi", "Right CM" )
implantation["depthLead"]["device"] = ("medtronic_3387", "medtronic_3387", "medtronic_3387", "medtronic_3387")

dl_fnames =  [ name.replace(" ", "_") for name in implantation["depthLead"]["name"] ]
implantation["depthLead"]["filename"] = dl_fnames

# transforms could be hard coded into networks
#implantation["depthLead"]["transforms"] =
#        {"rotation" : ("Left_depth_rotation.txt", "Left_depth_rotation.txt", "Right_depth_rotation.txt", "Right_depth_rotation.txt") }
#        {"translation" : ("Left_depth_translation.txt", "Left_depth_translation.txt", "Right_depth_translation.txt", "Right_depth_translation.txt") }


implantation["stripElectrodes"] = {
        "name" : ( "Left", "Right"),
        "filename": ("strip_left_plan.stl", "strip_right_plan.stl"),
        "orientation_file" : ( "contact_origin_left.txt", "contact_origin_right.txt")
}

# combining order: IPG, depth, strip

