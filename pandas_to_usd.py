from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import pandas as pd # might need to import this differently because it is in an extension
omni.kit.pipapi.install("Openpyxl", module="openpyxl")
import openpyxl

class PandasToUSD:
    def __init__(self):
        self._component_path = "/component_list_template.xlsx" # or user_path
        self._assemblies_path = "/assembly_list_template.xlsx" # or user_path
        self.components_df = None
        self.assemblies_df = None
        self.stage = omni.usd.get_context().get_stage()

    def set_kind(self,path,kind):
        omni.kit.commands.execute('ChangeMetadata',
                                  object_paths=[Sdf.Path(path)],
                                  key='kind',
                                  value=kind)

    def get_component_data(self,component_name):
        self.components_df = pd.read_excel(self._component_path)
        self.components_df.set_index('asset_name',inplace=True)
        return self.components_df.loc[component_name]

    def get_assembly_group_list(self):
        self.assemblies_df = pd.read_excel(self._assemblies_path)
        l_groups_non_duplicates = [*set(self.assemblies_df["group_name"])]
        return l_groups_non_duplicates

    def get_assembly_df(self):
        return pd.read_excel(self._assemblies_path)

    def get_assembly(self,assembly_name):
        self.assemblies_df = pd.read_excel(self._assemblies_path)

        assembly_sifting = self.assemblies_df[self.assemblies_df["group_name"]==assembly_name]

        for i in range(len(assembly_sifting)):
            _x_translate = assembly_sifting.iloc[i]['translate_x']
            _y_translate = assembly_sifting.iloc[i]['translate_y']
            _z_translate = assembly_sifting.iloc[i]['translate_z']

            _x_rotate = assembly_sifting.iloc[i]['rotation_x']
            _y_rotate = assembly_sifting.iloc[i]['rotation_y']
            _z_rotate = assembly_sifting.iloc[i]['rotation_z']

            _x_scale = assembly_sifting.iloc[i]['scale_x']
            _y_scale = assembly_sifting.iloc[i]['scale_y']
            _z_scale = assembly_sifting.iloc[i]['scale_z']

            group_name = assembly_sifting.iloc[i]['group_name']
            component_data = self.get_component_data(assembly_sifting.iloc[i]['component'])
            prim_reference_path = component_data["path"]
            attachment_type_attribute_value = component_data["component_type"]

            main_xform_name = f"/{group_name}"
            prim_xform_name = f"/{group_name}/{attachment_type_attribute_value}"
            prim_path_name = f"/{group_name}/{attachment_type_attribute_value}/{assembly_sifting.iloc[i]['component']}"

            main_xform = UsdGeom.Xform.Define(self.stage, main_xform_name)
            self.set_kind(main_xform.GetPath().pathString,"group")

            prim_xform = UsdGeom.Xform.Define(self.stage, prim_xform_name)
            self.set_kind(prim_xform.GetPath().pathString,"component")
            new_prim = self.stage.DefinePrim(prim_path_name)
            new_prim.GetReferences().AddReference(prim_reference_path)
            self.stage.SetDefaultPrim(new_prim)

            properties = new_prim.GetPropertyNames()
            if 'xformOp:translate' not in properties:
                UsdGeom.Xformable(new_prim).AddTranslateOp()
            if 'xformOp:rotateZYX' not in properties:
                UsdGeom.Xformable(new_prim).AddRotateZYXOp()
            if 'xformOp:scale' not in properties:
                UsdGeom.Xformable(new_prim).AddScaleOp()

            new_prim.GetAttribute('xformOp:rotateZYX').Set(Gf.Vec3f(_x_translate, _y_translate, _z_translate))
            new_prim.GetAttribute('xformOp:rotateZYX').Set(Gf.Vec3f(_x_rotate, _y_rotate, _z_rotate))
            new_prim.GetAttribute('xformOp:scale').Set(Gf.Vec3f(_x_scale, _y_scale, _z_scale))

    def create_all_assemblies(self):
        assemblies = self.get_assembly_group_list()
        for assembly in assemblies:
            self.get_assembly(assembly)

pandas_to_usd_machine = PandasToUSD()
pandas_to_usd_machine.create_all_assemblies()

