#!/pxrpythonsubst
#
# Copyright 2018 Pixar
#
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor
#    and its affiliates, except as required to comply with Section 4(c) of
#    the License and to reproduce the content of the NOTICE file.
#
# You may obtain a copy of the Apache License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.
#


import os
import unittest

from maya import cmds
from maya import standalone

from pxr import Usd
from pxr import UsdGeom
from pxr import Vt
from pxr import Gf


class testUsdExportParticles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        standalone.initialize('usd')

        cmds.file(os.path.abspath('UsdExportParticlesTest.ma'), open=True,
            force=True)

        cmds.loadPlugin('pxrUsd', quiet=True)

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    def testExportInstances(self):
        usdFile = os.path.abspath('UsdExportParticles_particles.usda')
        cmds.usdExport(mergeTransformAndShape=False, exportInstances=False,
            shadingMode='none', file=usdFile, frameRange=(1, 1))

        stage = Usd.Stage.Open(usdFile)

        p = UsdGeom.Points.Get(stage, '/particle1/particleShape1')
        self.assertTrue(p.GetPrim().IsValid())
        self.assertEqual(p.GetPointsAttr().Get(1), Vt.Vec3fArray(5, (Gf.Vec3f(5.0, 0.0, -6.0), Gf.Vec3f(-4.0, 0.0, -4.5), Gf.Vec3f(-4.5, 0.0, 3.0), Gf.Vec3f(-2.0, 0.0, 8.5), Gf.Vec3f(3.0, 0.0, 3.5))))
        self.assertEqual(p.GetVelocitiesAttr().Get(1), Vt.Vec3fArray(5, (Gf.Vec3f(0.0, 0.0, 0.0), Gf.Vec3f(1.0, 1.0, 1.0), Gf.Vec3f(2.0, 3.0, 4.0), Gf.Vec3f(5.0, 6.0, 7.0), Gf.Vec3f(8.0, 9.0, 10.0))))
        self.assertEqual(p.GetWidthsAttr().Get(1), Vt.FloatArray(5, (2.0, 2.0, 2.0, 2.0, 2.0)))
        self.assertEqual(p.GetIdsAttr().Get(1), Vt.Int64Array(5, (0, 1, 2, 3, 4)))

if __name__ == '__main__':
    unittest.main(verbosity=2)
