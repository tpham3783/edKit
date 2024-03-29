import unittest
import edleak.asset
import tempfile

allocer_list1 = [  {'id' : 0, 'stack' : [ 'caller1', 'caller2']},
              {'id' : 1, 'stack' : [ 'caller11', 'caller12']}]
slice_list1 = [ [ { 'mem' : 10, 'alc' : 0},
                  { 'mem' : 15, 'alc' : 1}],
                [ { 'mem' : 15, 'alc' : 0},
                  { 'mem' : 25, 'alc' : 1}],
                [ { 'mem' : 25, 'alc' : 0},
                  { 'mem' : 35, 'alc' : 1}],
                [ { 'mem' : 30, 'alc' : 0},
                  { 'mem' : 45, 'alc' : 1}]
            ]

class TestCaseEdleakAsset(unittest.TestCase):

   def setUp(self):
      self.seq = range(10)

   def test_build(self):
      asset = edleak.asset.Asset()
      self.assertIsNotNone(asset)

   def test_allocer_list(self):
      asset = edleak.asset.Asset()
      asset.setAllocerList(allocer_list1)
      self.assertEqual(asset.getAllocerList(), allocer_list1)

   def test_slice_list(self):
      asset = edleak.asset.Asset()
      asset.setSliceList(slice_list1)
      self.assertEqual(asset.getSliceList(), slice_list1)

   def test_save(self):
      file, name = tempfile.mkstemp()
      asset = edleak.asset.Asset()
      asset.setAllocerList(allocer_list1)
      asset.setSliceList(slice_list1)

      asset.save(name)
      asset2 = edleak.asset.Asset(name)
      self.assertEqual(asset.getSliceList(), asset2.getSliceList())
      self.assertEqual(asset.getAllocerList(), asset2.getAllocerList())

   def test_coring(self):
      asset = edleak.asset.Asset()
      asset.setAllocerList(allocer_list1)
      asset.setSliceList(slice_list1)

      allocer_list = asset.getAllocerList()
      self.assertEqual(slice_list1[0][0]['mem'], allocer_list[0]['coring'][0])
      self.assertEqual(slice_list1[0][1]['mem'], allocer_list[1]['coring'][0])
      self.assertEqual(slice_list1[1][0]['mem'], allocer_list[0]['coring'][1])
      self.assertEqual(slice_list1[1][1]['mem'], allocer_list[1]['coring'][1])
      self.assertEqual(slice_list1[2][0]['mem'], allocer_list[0]['coring'][2])
      self.assertEqual(slice_list1[2][1]['mem'], allocer_list[1]['coring'][2])
      self.assertEqual(slice_list1[3][0]['mem'], allocer_list[0]['coring'][3])
      self.assertEqual(slice_list1[3][1]['mem'], allocer_list[1]['coring'][3])

   def test_leak_factor(self):
      asset = edleak.asset.Asset()
      asset.setAllocerList(allocer_list1)
      asset.setSliceList(slice_list1)

      allocer_list = asset.getAllocerList()
      self.assertIsNotNone(allocer_list[0]['leak_factor'])

