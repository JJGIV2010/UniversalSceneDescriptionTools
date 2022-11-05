from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

#
"""
always use model heirarchy: assembly/group - component/subcomponent

Only group model prims can have other model children (assembly is a kind of group)

A prim can only be a model if its parent prim is also a (group) model - except for the root model prim.

No prim should have the exact kind “model”, because “model” is neither a singular component nor a plural group container - it is just the “abstract” commonality between components and groups.
"""

class usd_workflow:
    def __init__(self):
        self.prim_name = ""
        self.stage = omni.usd.get_context().get_stage()
    
    def add_comment(self,prim_path,text):
        prim = self.stage.GetPrimAtPath(prim_path)
        prim.SetMetadata('comment',text)

    def set_kind(self,path,kind):
        prim = self.stage.GetPrimAtPath(path)
        omni.kit.commands.execute('ChangeMetadata',
                                  object_paths=[Sdf.Path('/World/Cone')],
                                  key='kind',
                                  value=kind)

    def get_kind(self,path):
        prim = self.stage.GetPrimAtPath(path)
        v = Usd.ModelAPI(prim).GetKind()
        print('[ ' + prim.GetName() + ' ] Kind = ' + v)

    def _show_as_string(self):
        print(self.stage.GetRootLayer().ExportToString())




test = usd_workflow()

test._show_as_string()

