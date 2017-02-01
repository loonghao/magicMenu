import os
import unittest

import pixoConfig
import pixoFileTools as pft


def makeSite(site):
    pixoConfig.PixoConfig.data = None
    pft.PathDetails.datare = None
    pft.PathDetails.path_strings = None

    f = pixoConfig.PixoConfig.get_local_site_filepath()
    old_value = None
    if os.path.exists(f):
        with open(f) as file_stream:
            old_value = file_stream.read()

    with open(f, "w") as file_stream:
        file_stream.write(site)
    return old_value


def restoreSite(site):
    f = pixoConfig.PixoConfig.get_local_site_filepath()
    if site is None:
        os.remove(f)
    else:
        with open(f, "w") as file_stream:
            file_stream.write(site)


class PixoFileToolTestsPEK(unittest.TestCase):
    old_site = None

    @classmethod
    def setUpClass(cls):
        PixoFileToolTestsPEK.old_site = makeSite("PEK")

    @classmethod
    def tearDownClass(cls):
        restoreSite(PixoFileToolTestsPEK.old_site)

    def test_pek_asset_pathone(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_filename()
        print x
        self.assertEqual(x.project, "ants")
        self.assertEqual(x.project_shortname, "ant")
        self.assertEqual(x.seq, "creature")
        self.assertEqual(x.shot, "crt_kingKong")
        self.assertEqual(x.version, "005")
        self.assertEqual(x.task, "mdl")
        self.assertEqual(x.user, "hal")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, os.path.basename(f1))
        response = x.get_full_path()
        self.assertEqual(response, f1)

    def test_pek_comp_path(self):
        f1 = "Y:/impossibletwo_ipt-3444/b020/070/comps/v131/fullres/ipt_b020_070_comp_v131_zxy.1001.exr"
        x = pft.PathDetails.parse_path(f1)
        print x
        self.assertEqual(x.project, "impossibletwo")
        self.assertEqual(x.project_shortname, "ipt")
        self.assertEqual(x.seq, "b020")
        self.assertEqual(x.shot, "070")
        self.assertEqual(x.version, "131")
        self.assertEqual(x.task, "comp")
        self.assertEqual(x.user, "zxy")
        self.assertEqual(x.ext, "exr")
        response = x.get_full_path()
        self.assertEqual(response, f1)




    def test_pek_asset_pathone_publish(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_publish_full_path()

        p1 = 'X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/_publish/' \
             'v005/ant_crt_kingKong_mdl_v005_hal.ma'
        p2 = 'X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/_publish/' \
             'v005/ant_crt_kingKong_mdl_playblast_v005_hal.ma'
        self.assertEqual(response, p1)
        response = x.get_publish_full_path(name="playblast")
        self.assertEqual(response, p2)
        x = pft.PathDetails.parse_path(p2)
        response = x.get_publish_full_path(name="playblast")
        self.assertEqual(response, p2)
        response = x.get_publish_full_path()
        self.assertEqual(response, p2)
        response = x.get_publish_full_path(name=None)
        self.assertEqual(response, p1)

    def test_pek_asset_pathone_render(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        f2 = "Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_render_path()
        self.assertEqual(response, f2)

        p1 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/fullres/ant_crt_kingKong_mdl_playblast_v005_hal.####.exr'

        p2 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/fullres/ant_crt_kingKong_mdl_v005_hal.####.exr'

        x = pft.PathDetails.parse_path(p2)

        response = x.get_render_full_path(name="playblast")
        self.assertEqual(response, p1)
        response = x.get_render_full_path()
        self.assertEqual(response, p1)
        response = x.get_render_full_path(name=None)
        self.assertEqual(response, p2)

        x = pft.PathDetails.parse_path(f1)
        response = x.get_render_full_path(name="playblast", render_layer="layerssuck", resolution='resolution')
        p1 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/layerssuck/resolution/ant_crt_kingKong_mdl_playblast_v005_hal.####.exr'
        p2 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/resolution/ant_crt_kingKong_mdl_playblast_v005_hal.####.exr'
        proxy = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/v005' \
                '/resolution/ant_crt_kingKong_mdl_playblast_v005_hal.mov'\

        self.assertEqual(response, p1)
        y = pft.PathDetails.parse_path(p1)
        response = y.get_render_full_path(name="playblast", render_layer=None)
        self.assertEqual(response, p2)

        response = y.get_render_proxy_object("playblast")
        r2 = response.get_full_path()
        self.assertEqual(r2, proxy)

    def test_pek_shots_pathone_render(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/anim/icf_000_animpipe_anim_v004_car.ma"
        p1 = "Y:/icefantasy_icf-3595/000/animpipe/elements/3d/anim/v004/fullres/icf_000_animpipe_anim_beauty_v004_car.####.exr"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_render_full_path(name="beauty")
        self.assertEqual(response, p1)

    def test_pek_version_up(self):
        f1 = "X:/icefantasy_icf-3595/_library/assets/creature/crt_iceBird/cgfx_fur/icf_crt_iceBird_cgfx_fur_v071_mil.ma"
        x = pft.PathDetails.parse_path(f1)
        self.assertEqual(x.shot, "crt_iceBird")
        self.assertEqual(x.task, "cgfx_fur")

    def test_pek_shots_pathone(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/anim/icf_000_animpipe_anim_v004_car.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_full_path()
        self.assertEqual(x.project, "icefantasy")
        self.assertEqual(x.project_shortname, "icf")
        self.assertEqual(x.seq, "000")
        self.assertEqual(x.shot, "animpipe")
        self.assertEqual(x.version, "004")
        self.assertEqual(x.task, "anim")
        self.assertEqual(x.user, "car")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, f1)
        response = x.get_filename()
        self.assertEqual(response, os.path.basename(f1))

    def test_pek_asset_pathtwo(self):
        f1 = "X:/ants_ant-3629/_library/assets/characters/chr_DXDaily/mdl/ant_chr_DXDaily_mdl_v002.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_full_path()
        self.assertEqual(x.project, "ants")
        self.assertEqual(x.project_shortname, "ant")
        self.assertEqual(x.seq, "characters")
        self.assertEqual(x.shot, "chr_DXDaily")
        self.assertEqual(x.version, "002")
        self.assertEqual(x.task, "mdl")
        self.assertEqual(x.user, "bdl")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, f1)
        response = x.get_filename()
        self.assertEqual(response, os.path.basename(f1))

    def test_pek_shots_pathtwo(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/cgfx_lingering-dust-slap/icf_000_animpipe_cgfx_lingering-dust-slap_v004_car.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_full_path()
        self.assertEqual(x.project, "icefantasy")
        self.assertEqual(x.project_shortname, "icf")
        self.assertEqual(x.seq, "000")
        self.assertEqual(x.shot, "animpipe")
        self.assertEqual(x.version, "004")
        self.assertEqual(x.task, "cgfx_lingering-dust-slap")
        self.assertEqual(x.user, "car")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, f1)
        response = x.get_filename()
        self.assertEqual(response, os.path.basename(f1))

    def test_pek_shots_paththree(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/cgfx_lingering-dust-slap"
        x = pft.PathDetails.parse_path(f1)
        response = x.get_path()
        self.assertEqual(x.project, "icefantasy")
        self.assertEqual(x.project_shortname, "icf")
        self.assertEqual(x.seq, "000")
        self.assertEqual(x.shot, "animpipe")
        self.assertEqual(x.task, "cgfx_lingering-dust-slap")
        self.assertEqual(response, f1)

    def test_pek_asset_deconstructFilepath(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        root, show, seq, shot, category, task, filename = pft.deconstruct_filepath(f1)

        self.assertEqual(root, "X:")
        self.assertEqual(show, "ants_ant-3629")
        self.assertEqual(seq, "creature")
        self.assertEqual(shot, "crt_kingKong")
        self.assertEqual(task, "mdl")
        self.assertEqual(category, "assets")
        self.assertEqual(filename, "ant_crt_kingKong_mdl_v005_hal.ma")

        response = pft.construct_filepath(root, show, seq, shot, category, task, filename)
        r2 = pft.construct_filename("ant", seq, shot, task, "v005", "hal", "ma", category)
        self.assertEqual(response, f1)
        self.assertEqual(r2, os.path.basename(f1))


    def test_pek_shots_deconstructFilepath(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/anim/icf_000_animpipe_anim_v004_car.ma"

        root, show, seq, shot, category, task, publish = pft.deconstruct_filepath(f1)
        self.assertEqual(show, "icefantasy_icf-3595")
        self.assertEqual(seq, "000")
        self.assertEqual(shot, "animpipe")
        self.assertEqual(task, "anim")
        self.assertEqual(category, "3d")
        self.assertEqual(publish, 'icf_000_animpipe_anim_v004_car.ma')

        response = pft.construct_filepath(root, show, seq, shot, category, task, publish)
        self.assertEqual(response, f1)

    def test_pek_comp_parseeye(self):
        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj_R.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal_R.0960.exr"
             ]
        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals("R", result.eye)

        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj_L.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal_L.0960.exr"
             ]

        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals("L", result.eye)

        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal.0960.exr"
             ]

        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals(None, result.eye)

    def test_comp_render_path(self):
        f = [
            'Y:/number6_nm6-3727/prv/0010/comps/v007/fullres/nm6_prv_0010_comp_v007_qqh.####.exr',
            'X:/number6_nm6-3727/prv/0010/2d/comp/nm6_prv_0010_comp_v007_qqh.nk'
        ]
        for path in f:
            result = pft.PathDetails.parse_path(path)
            self.assertEquals(path, result.get_full_path())
            self.assertEquals(f[0], result.get_render_full_path())

    def test_comp_subtaks_render_path(self):
        files = [
            'X:/alibabablossom_bls-3597/es/0030/2d/comp-setup/bls_es_0030_comp-setup_ud_v001_flr.nk',
            'X:/alibabablossom_bls-3597/es/0030/2d/comp-matte/bls_es_0030_comp-matte_v001_flr.nk',
            'X:/alibabablossom_bls-3597/es/0030/2d/comp-slap/bls_es_0030_comp-slap_v001_flr.nk',
        ]
        renders = [
            'Y:/alibabablossom_bls-3597/es/0030/elements/2d/comp-setup/v001/fullres/bls_es_0030_comp-setup_ud_v001_flr.####.exr',
            'Y:/alibabablossom_bls-3597/es/0030/elements/2d/comp-matte/v001/fullres/bls_es_0030_comp-matte_v001_flr.####.exr',
            'Y:/alibabablossom_bls-3597/es/0030/elements/2d/comp-slap/v001/fullres/bls_es_0030_comp-slap_v001_flr.####.exr'
        ]
        for i, f in enumerate(files):
            result = pft.PathDetails.parse_path(f)
            print result.get_render_full_path()
            self.assertEquals(f, result.get_full_path())
            self.assertEquals(renders[i], result.get_render_full_path())


    def test_pek_comp_parse(self):
        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal_R.0960.exr"
             ]
        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals(p, result.get_full_path())

    def test_nuke_subtask1(self):
        path = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime_plateA/bls_es_1180_comp-retime_plateA_v001_car.nk'
        f1 = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime_plateA/_publish/v001/bls_es_1180_comp-retime_plateA_v001_car.nk'
        dets = pft.PathDetails.parse_path(path)
        self.assertEquals(f1, dets.get_publish_full_path())

    def test_nuke_subtask2(self):
        path = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime/bls_es_1180_comp-retime_plateA_v001_car.nk'
        f1 = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime/_publish/v001/bls_es_1180_comp-retime_plateA_v001_car.nk'
        dets = pft.PathDetails.parse_path(path)
        self.assertEquals(f1, dets.get_publish_full_path())

    def test_some_different_task_name1(self):
        f = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_master_camera_v009_evl.ma'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam'
        p2 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/bls_es_0140_cam_master_camera_v009_evl.ma'
        p3 = 'Y:/alibabablossom_bls-3597/es/0140/elements/3d/cam/v009/fullres/bls_es_0140_cam_master_camera_v009_evl.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_master_camera_v009_evl.ma'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())
        obj = dets.get_publish_path_object()
        obj.name = 'camera_master-dd-jj-yy'
        p5 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_camera_master-dd-jj-yy_v009_evl.ma'
        self.assertEqual(p5, obj.get_full_path())

        obj = dets.get_working_path_object()
        obj.name = 'camera_master-dd-jj-yy'
        p6 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/bls_es_0140_cam_camera_master-dd-jj-yy_v009_evl.ma'
        self.assertEqual(p6, obj.get_full_path())

        obj = dets.get_render_path_object()
        obj.render_layer = 'render_layer'
        obj.name = 'camera_master-dd-jj-yy'
        p7 = 'Y:/alibabablossom_bls-3597/es/0140/elements/3d/cam/render_layer/v009/fullres/bls_es_0140_cam_camera_master-dd-jj-yy_v009_evl.####.exr'
        self.assertEqual(p7, obj.get_render_full_path())


    def test_some_different_task_name2(self):
        f = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_v009_evl.bak'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam'
        p2 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/bls_es_0140_cam_v009_evl.bak'
        p3 = 'Y:/alibabablossom_bls-3597/es/0140/elements/3d/cam/v009/fullres/bls_es_0140_cam_v009_evl.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_v009_evl.bak'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())
        obj = dets.get_publish_path_object()
        obj.name = 'camera_master-dd-jj-yy'
        p5 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_camera_master-dd-jj-yy_v009_evl.bak'
        self.assertEqual(p5, obj.get_full_path())

        obj = dets.get_working_path_object()
        obj.name = 'camera_master-dd-jj-yy'
        p6 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/bls_es_0140_cam_camera_master-dd-jj-yy_v009_evl.bak'
        self.assertEqual(p6, obj.get_full_path())

        obj = dets.get_render_path_object()
        obj.render_layer = 'render_layer'
        obj.name = 'camera_master-dd-jj-yy'
        p7 = 'Y:/alibabablossom_bls-3597/es/0140/elements/3d/cam/render_layer/v009/fullres/bls_es_0140_cam_camera_master-dd-jj-yy_v009_evl.####.exr'
        self.assertEqual(p7, obj.get_render_full_path())

    def test_some_different_task_name3(self):
        f = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_stereo_camera_v009_evl.pfo'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam'
        p2 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/bls_es_0140_cam_stereo_camera_v009_evl.pfo'
        p3 = 'Y:/alibabablossom_bls-3597/es/0140/elements/3d/cam/v009/fullres/bls_es_0140_cam_stereo_camera_v009_evl.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/es/0140/3d/cam/_publish/v009/bls_es_0140_cam_stereo_camera_v009_evl.pfo'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())

    def test_some_different_task_name4(self):
        f = 'X:/alibabablossom_bls-3597/es/0060/3d/anim_fishGroup/_publish/v011/bls_es_0060_anim_fishGroup_crt_YellowfinTuna8-uu-jjj_v011_evl.pfo'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/es/0060/3d/anim_fishGroup'
        p2 = 'X:/alibabablossom_bls-3597/es/0060/3d/anim_fishGroup/bls_es_0060_anim_fishGroup_crt_YellowfinTuna8-uu-jjj_v011_evl.pfo'
        p3 = 'Y:/alibabablossom_bls-3597/es/0060/elements/3d/anim_fishGroup/v011/fullres/bls_es_0060_anim_fishGroup_crt_YellowfinTuna8-uu-jjj_v011_evl.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/es/0060/3d/anim_fishGroup/_publish/v011/bls_es_0060_anim_fishGroup_crt_YellowfinTuna8-uu-jjj_v011_evl.pfo'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())

    def test_some_different_task_name5(self):
        f = 'X:/alibabablossom_bls-3597/es/0600/3d/mm/_publish/v004/bls_es_0600_mm_master_camera_v004_car.ma'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/es/0600/3d/mm'
        p2 = 'X:/alibabablossom_bls-3597/es/0600/3d/mm/bls_es_0600_mm_master_camera_v004_car.ma'
        p3 = 'Y:/alibabablossom_bls-3597/es/0600/elements/3d/mm/v004/fullres/bls_es_0600_mm_master_camera_v004_car.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/es/0600/3d/mm/_publish/v004/bls_es_0600_mm_master_camera_v004_car.ma'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())

    def test_some_different_task_name6(self):
        f = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime/bls_es_1180_comp-retime_plateA_v001_car.nk'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime'
        p2 = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime/bls_es_1180_comp-retime_plateA_v001_car.nk'
        p3 = 'Y:/alibabablossom_bls-3597/es/1180/elements/2d/comp-retime/v001/fullres/bls_es_1180_comp-retime_plateA_v001_car.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/es/1180/2d/comp-retime/_publish/v001/bls_es_1180_comp-retime_plateA_v001_car.nk'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())

    def test_some_different_task_name7(self):
        f = 'X:/alibabablossom_bls-3597/es/0060/2d/comp/bls_es_0060_comp_v001_thl.nk'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/es/0060/2d/comp'
        p2 = 'X:/alibabablossom_bls-3597/es/0060/2d/comp/bls_es_0060_comp_v001_thl.nk'
        p3 = 'Y:/alibabablossom_bls-3597/es/0060/comps/v001/fullres/bls_es_0060_comp_v001_thl.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/es/0060/2d/comp/_publish/v001/bls_es_0060_comp_v001_thl.nk'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())

    def test_some_different_task_name8(self):
        f = 'X:/alibabablossom_bls-3597/_library/assets/characters/chr_manA/mdl/_publish/v001/bls_chr_manA_mdl_v001_yga.ma'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/_library/assets/characters/chr_manA/mdl'
        p2 = 'X:/alibabablossom_bls-3597/_library/assets/characters/chr_manA/mdl/bls_chr_manA_mdl_v001_yga.ma'
        p3 = 'Y:/alibabablossom_bls-3597/_library/assets/characters/chr_manA/renders/mdl/v001/fullres/bls_chr_manA_mdl_v001_yga.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/_library/assets/characters/chr_manA/mdl/_publish/v001/bls_chr_manA_mdl_v001_yga.ma'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())

    def test_some_different_task_name9(self):
        f = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_lo/_publish/v001/bls_prp_patchB_mdl_lo_v001_cre.abc'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_lo'
        p2 = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_lo/bls_prp_patchB_mdl_lo_v001_cre.abc'
        p3 = 'Y:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/renders/mdl_lo/v001/fullres/bls_prp_patchB_mdl_lo_v001_cre.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_lo/_publish/v001/bls_prp_patchB_mdl_lo_v001_cre.abc'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())

    def test_some_different_task_name10(self):
        f = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_vrproxy/_publish/v011/bls_prp_patchB_mdl_vrproxy_v011_car.ma'
        dets = pft.PathDetails.parse_path(f)
        p1 = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_vrproxy'
        p2 = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_vrproxy/bls_prp_patchB_mdl_vrproxy_v011_car.ma'
        p3 = 'Y:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/renders/mdl_vrproxy/v011/fullres/bls_prp_patchB_mdl_vrproxy_v011_car.####.exr'
        p4 = 'X:/alibabablossom_bls-3597/_library/assets/props/prp_patchB/mdl_vrproxy/_publish/v011/bls_prp_patchB_mdl_vrproxy_v011_car.ma'
        self.assertEqual(f, dets.get_full_path())
        self.assertEqual(p1, dets.get_working_path())
        self.assertEqual(p2, dets.get_working_full_path())
        self.assertEqual(p3, dets.get_render_full_path())
        self.assertEqual(p4, dets.get_publish_full_path())


    """
    def test_version_up(self):

        temp_path = tempfile.mkdtemp()
        print temp_path
        files = [
                 "test_v001_ben.ma",
                 "test_v002_blah.ma",
                 "test_v002_bob.ma",
                 "test_v003_blah.ma"
                 ]
        for x in files:
            pft.touch(os.path.join(temp_path, x))

        result = pft.get_latest_version_number(temp_path)
        self.assertEquals(result, "003")


    def test_incremental_version_up(self):

        temp_path = tempfile.mkdtemp()
        print temp_path
        files = [
            "test_v001_ben.ma",
            "test_v002_blah.ma",
            "test_v002-001_blah.ma",
            "test_v002-002_blah.ma",
            "test_v002_bob.ma",
            "test_v003_blah.ma",
            "test_v003-001_blah.ma"
        ]
        for x in files:
            pft.touch(os.path.join(temp_path, x))

        result = pft.get_latest_version_number(temp_path)
        self.assertEquals(result, "004")
    """

if __name__ == '__main__':
    unittest.main()
