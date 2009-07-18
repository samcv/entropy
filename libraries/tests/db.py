# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'.')
sys.path.insert(0,'../')
import unittest
import os
from entropy.client.interfaces import Client
from entropy.const import etpConst, etpUi
from entropy.core import SystemSettings
from entropy.db import EntropyRepository
import _misc

class EntropyRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.Client = Client(noclientdb = 2, indexing = False, xcache = False,
            repo_validation = False)
        self.Spm = self.Client.Spm()
        self.test_db_name = "%s_test_suite" % (etpConst['dbnamerepoprefix'],)
        self.client_sysset_plugin_id = \
            etpConst['system_settings_plugins_ids']['client_plugin']
        self.test_db = self.__open_test_db()
        self.SystemSettings = SystemSettings()

    def tearDown(self):
        """
        tearDown is run after each test
        """
        sys.stdout.write("%s ran\n" % (self,))
        sys.stdout.flush()
        self.test_db.closeDB()
        self.Client.destroy()

    def __open_test_db(self):
        return self.Client.open_memory_database(dbname = self.test_db_name)

    def test_db_creation(self):
        self.assert_(isinstance(self.test_db, EntropyRepository))
        self.assertEqual(self.test_db_name,self.test_db.dbname)
        self.assert_(self.test_db.doesTableExist('baseinfo'))
        self.assert_(self.test_db.doesTableExist('extrainfo'))

    def test_db_insert_compare_match(self):

        # insert/compare
        test_pkg = _misc.get_test_package()
        data = self.Spm.extract_pkg_metadata(test_pkg, silent = True)
        idpackage, rev, new_data = self.test_db.handlePackage(data)
        db_data = self.test_db.getPackageData(idpackage)
        self.assertEqual(new_data, db_data)

        # match
        nf_match = (-1, 1)
        f_match = (1, 0)
        pkg_atom = _misc.get_test_package_atom()
        pkg_name = _misc.get_test_package_name()
        self.assertEqual(nf_match, self.test_db.atomMatch("slib"))
        self.assertEqual(f_match,
            self.test_db.atomMatch(pkg_name))
        self.assertEqual(f_match,
            self.test_db.atomMatch(pkg_atom))

        # test package masking
        plug_id = self.client_sysset_plugin_id
        masking_validation = \
            self.SystemSettings[plug_id]['masking_validation']['cache']
        f_match_mask = (1, 
            self.test_db_name[len(etpConst['dbnamerepoprefix']):],)

        self.SystemSettings['live_packagemasking']['mask_matches'].add(
            f_match_mask)
        masking_validation.clear()
        self.assertEqual((-1, 1),self.test_db.atomMatch(pkg_atom))

        self.SystemSettings['live_packagemasking']['mask_matches'].discard(
            f_match_mask)
        masking_validation.clear()
        self.assertNotEqual((-1, 1),self.test_db.atomMatch(pkg_atom))

        # now test multimatch
        idpackage, rev, new_data = self.test_db.addPackage(db_data,
            do_remove = False)
        results, rc = self.test_db.atomMatch(pkg_name, multiMatch = True)
        self.assertEqual(2, len(results))
        self.assert_(type(results) is set)
        self.assert_(rc == 0)

        results, rc = self.test_db.atomMatch(pkg_name+"foo", multiMatch = True)
        self.assertEqual(0, len(results))
        self.assert_(type(results) is set)
        self.assert_(rc == 1)

    def test_db_insert_compare_match_utf(self):

        # insert/compare
        test_pkg = _misc.get_test_package2()
        data = self.Spm.extract_pkg_metadata(test_pkg, silent = True)
        # Portage stores them this way
        data['changelog'] = u"#248083).\n\n  06 Feb 2009; Ra\xc3\xbal Porcel"
        data['license'] = u'GPL-2'
        data['licensedata'] = {
            u'GPL-2': u"#248083).\n\n  06 Feb 2009; Ra\xc3\xbal Porcel",
        }
        idpackage, rev, new_data = self.test_db.handlePackage(data)
        db_data = self.test_db.getPackageData(idpackage)
        self.assertEqual(new_data, db_data)

        # match
        nf_match = (-1, 1)
        f_match = (1, 0)
        pkg_atom = _misc.get_test_package_atom2()
        pkg_name = _misc.get_test_package_name2()
        self.assertEqual(nf_match, self.test_db.atomMatch("slib"))
        self.assertEqual(f_match,
            self.test_db.atomMatch(pkg_name))
        self.assertEqual(f_match,
            self.test_db.atomMatch(pkg_atom))

        # test package masking
        plug_id = self.client_sysset_plugin_id
        masking_validation = \
            self.SystemSettings[plug_id]['masking_validation']['cache']
        f_match_mask = (1, 
            self.test_db_name[len(etpConst['dbnamerepoprefix']):],)

        self.SystemSettings['live_packagemasking']['mask_matches'].add(
            f_match_mask)
        masking_validation.clear()
        self.assertEqual((-1, 1),self.test_db.atomMatch(pkg_atom))

        self.SystemSettings['live_packagemasking']['mask_matches'].discard(
            f_match_mask)
        masking_validation.clear()
        self.assertNotEqual((-1, 1),self.test_db.atomMatch(pkg_atom))

    def test_db_insert_compare_match_utf2(self):

        # insert/compare
        test_pkg = _misc.get_test_package3()
        data = self.Spm.extract_pkg_metadata(test_pkg, silent = True)
        idpackage, rev, new_data = self.test_db.handlePackage(data)
        db_data = self.test_db.getPackageData(idpackage)
        self.assertEqual(new_data, db_data)

        # match
        nf_match = (-1, 1)
        f_match = (1, 0)
        pkg_atom = _misc.get_test_package_atom3()
        pkg_name = _misc.get_test_package_name3()
        self.assertEqual(nf_match, self.test_db.atomMatch("slib"))
        self.assertEqual(f_match,
            self.test_db.atomMatch(pkg_name))
        self.assertEqual(f_match,
            self.test_db.atomMatch(pkg_atom))

        # test package masking
        plug_id = self.client_sysset_plugin_id
        masking_validation = \
            self.SystemSettings[plug_id]['masking_validation']['cache']
        f_match_mask = (1, 
            self.test_db_name[len(etpConst['dbnamerepoprefix']):],)

        self.SystemSettings['live_packagemasking']['mask_matches'].add(
            f_match_mask)
        masking_validation.clear()
        self.assertEqual((-1, 1),self.test_db.atomMatch(pkg_atom))

        self.SystemSettings['live_packagemasking']['mask_matches'].discard(
            f_match_mask)
        masking_validation.clear()
        self.assertNotEqual((-1, 1),self.test_db.atomMatch(pkg_atom))

    def test_db_import_export(self):

        test_pkg = _misc.get_test_package2()
        data = self.Spm.extract_pkg_metadata(test_pkg, silent = True)
        # Portage stores them this way
        data['changelog'] = u"#248083).\n\n  06 Feb 2009; Ra\xc3\xbal Porcel"
        data['license'] = u'GPL-2'
        data['licensedata'] = {
            u'GPL-2': u"#248083).\n\n  06 Feb 2009; Ra\xc3\xbal Porcel",
        }
        idpackage, rev, new_data = self.test_db.handlePackage(data)
        db_data = self.test_db.getPackageData(idpackage)
        self.assertEqual(new_data, db_data)

        etpUi['mute'] = True

        # export
        buf_file = "dbtst.txt"
        buf = open(buf_file,"w")
        self.test_db.doDatabaseExport(buf)
        buf.flush()
        buf.close()

        new_db_path = "test_db_import_export.db"
        self.test_db.doDatabaseImport(buf_file, new_db_path)
        new_db = self.Client.open_generic_database(new_db_path)
        new_db_data = new_db.getPackageData(idpackage)
        new_db.closeDB()
        etpUi['mute'] = False
        self.assertEqual(new_db_data, db_data)
        os.remove(buf_file)
        os.remove(new_db_path)


    def test_db_package_sets(self):

        set_name = 'my_test_set'
        set_deps = ["app-foo/foo","app-pling/plong","media-foo/ajez"]
        set_name2 = 'my_test_set2'
        set_deps2 = ["app-foo/foo2","app-pling/plong2","media-foo/ajez2"]
        pkgsets = {
            set_name: set(set_deps),
            set_name2: set(set_deps2),
        }
        self.test_db.insertPackageSets(pkgsets)
        self.assertEqual(self.test_db.retrievePackageSets(), pkgsets)
        set_search = self.test_db.searchSets(set_name2)
        self.assertEqual(set([set_name2]),set_search)

    def test_db_license_data_str_insert(self):
        lic_txt = '[3]\xab foo\n\n'
        lic_data = {u'CCPL-Attribution-2.0': lic_txt}
        self.test_db.insertLicenses(lic_data)
        db_lic_txt = self.test_db.retrieveLicenseText('CCPL-Attribution-2.0')
        self.assertEqual(db_lic_txt, lic_txt)

    # XXX complete

if __name__ == '__main__':
    unittest.main()
