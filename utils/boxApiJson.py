from boxsdk import JWTAuth, Client
import time
import gzip
import zlib
from io import BytesIO
# import io
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


class BoxApiJson:

    def __init__(self, jsonPath):
        self.jsonPath = jsonPath
        self._createClient()

    def _createClient(self):
        auth = JWTAuth.from_settings_file(self.jsonPath)
        self.client = Client(auth)

    def downloadFile(self, fileId, filePath):
        '''
        This will replace the file if it already exist in your local path 
        '''
        # self._createClient()
        # check if access token is valid
        with open(filePath, 'wb') as open_file:
            self.client.file(fileId).download_to(open_file)
            open_file.close()

    def readTxt(self, fileId):
        # self._createClient()
        txt = self.client.file(fileId).content().decode("utf-8")
        return txt

    def readGzipParquet(self, fileId):
        # self._createClient()
        gzip_file = self.client.file(fileId).content()
        # time.sleep(1)
        parquet_file = pq.ParquetFile(BytesIO(gzip_file))
        table = parquet_file.read()
        df = table.to_pandas()
        return df

    def uploadParquetDirectly(self, df, fileName, folderId):
        # self._createClient()
        parquet_data = BytesIO()
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_data, compression='gzip')

        parquet_io = BytesIO(parquet_data.getvalue())

        gzip_data = BytesIO()
        with gzip.GzipFile(fileobj=gzip_data, mode='wb') as gz:
            gz.write(parquet_io.getvalue())

        gzip_io = BytesIO(gzip_data.getvalue())

        self.client.folder(folderId).upload_stream(gzip_data, fileName)

    def downloadFileByName(self, folderId, fileName):
        '''
            to download a file using the name only 
        '''
        # self._createClient()
        # get items
        items_in_folder = self.getItemsFromFolder(folderId=folderId)
        # download file
        for item in items_in_folder:
            if item['item_name'] == fileName:
                self.downloadFile(fileId=item['item_id'], filePath=fileName)

    def uploadNewFile(self, filePath, folderId):
        '''
        If the file exist this will failed 
        This will return the dictionary:
            {'newFileName': newFile.name,
                'newFileId': newFile.id}
        '''
        # self._createClient()
        newFile = self.client.folder(folderId).upload(filePath)
        time.sleep(1)

        return {'newFile': newFile.name, 'newFileId': newFile.id}

    def uploadFileVersion(self, filePath, fileId):
        '''
        Upload a new version of a file already in box 

        '''
        # self._createClient()
        updatedFile = self.client.file(fileId).update_contents(filePath)

    def uploadNewOrVersion(self, folderId, fileName, filePath):
        # get items
        # self._createClient()
        items = self.getItemsFromFolder(folderId)
        for item in items:
            if item['item_name'] == fileName:
                self.uploadFileVersion(
                    filePath=filePath, fileId=item['item_id'])
                return 'File Version Uploaded'

        self.uploadNewFile(filePath=filePath, folderId=folderId)
        return 'New File Uploaded'

    def getItemsFromFolder(self, folderId):
        '''
            This will get the folders inside a master folder
            This will return a list of dictionaries with all the items in a folder 
        '''
        # self._createClient()
        items = self.client.folder(folder_id=folderId).get_items()
        itemList = []
        for item in items:
            itemRecord = {
                'item_type': item.type.capitalize(),
                'item_id': item.id,
                'item_name': item.name
            }
            # if itemRecord['item_type'] == 'Folder':
            itemList.append(itemRecord)
        return itemList

    def createNewFolder(self, masterFolderId, subFolderName):
        # self._createClient()
        try:
            subfolder = self.client.folder(
                masterFolderId).create_subfolder(subFolderName)
            print('Created subfolder with ID {0}'.format(subfolder.id))
            return subfolder.id
        except:
            print('folder already exist')
            return None

    def getFolderInfo(self, folderId):
        # self._createClient()
        # self._checkAccessToken()
        folder = self.client.folder(folder_id=folderId).get()
        folderInfo = {
            'folderName': folder.name,
            'folderId': folderId,
            'createdTime': folder.created_at
        }
        return folderInfo
