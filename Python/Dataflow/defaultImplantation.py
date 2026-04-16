# default/example implantation profile

def_implantation = { "geom_dir" : "SCIRun_files/ImplantGeoms" }

def_implantation["configuration"] = {
  "IPG": "twoIPG",
  "depthLead" : "fourLead",
  "stripElectrodes": "twoStrips"
}
def_implantation["IPG"] = {
            "name" : ( "Left" , "Right"),
            "filename": ( "IPG_left_plan.stl", "IPG_right_plan.stl" )
}

def_implantation["depthLead"] = {}
def_implantation["depthLead"]["name"] = ("Left GPi", "Left CM", "Right GPi", "Right CM" )
def_implantation["depthLead"]["device"] = ("medtronic_3387", "medtronic_3387", "medtronic_3387", "medtronic_3387")

dl_fnames =  [ name.replace(" ", "_") for name in def_implantation["depthLead"]["name"] ]
def_implantation["depthLead"]["filename"] = dl_fnames

def_implantation["stripElectrodes"] = {
        "name" : ( "Left", "Right"),
        "filename": ("strip_left_plan.stl", "strip_right_plan.stl"),
        "orientation_file" : ( "contact_origin_left.txt", "contact_origin_right.txt")
}

