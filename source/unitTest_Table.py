import unittest
from types import SimpleNamespace
from cursedIbreW import *

class unitTest_People(unittest.TestCase):
    def test_calc_table_width(self):
        #Arrange
        title = "Testing"
        dataList = []
        obj = SimpleNamespace(displayName='Short')
        dataList.append(obj)
        obj = SimpleNamespace(displayName='Medium')
        dataList.append(obj)
        obj = SimpleNamespace(displayName='Longgggg')
        dataList.append(obj)
        obj = SimpleNamespace(displayName='VEEEEEEEERRRRRRYYYYYYY LOOOOOOOOOOONNNNNGGGGGGG')
        dataList.append(obj)
        expected_output = len(dataList[3].displayName)
        #Act
        actual_output = calcTableWidth(title,dataList)
        #Assert
        self.assertEqual(expected_output,actual_output)

    def test_filter_table_1(self):
        #Arrange
        obj1 = SimpleNamespace(displayName='David')
        obj2 = SimpleNamespace(displayName='Dave')
        obj3 = SimpleNamespace(displayName='Henry')
        test_peeps = [obj1,obj2,obj3]
        #Act
        filtered_peeps = filterTable(test_peeps,"D")
        #Assert
        self.assertEqual(2,len(filtered_peeps))
if __name__ == "__main__":
    unittest.main()