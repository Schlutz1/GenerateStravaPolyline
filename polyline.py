class PolylineHandler():

    def decodePolylineData(self, mapData):
        ''' Decodes polyline data into latlong array '''

        if isinstance(mapData, str):
            mapData = ast.literal_eval(mapData)

        return polyline.decode(mapData['summary_polyline'])

    def filterAnomalousPolylineData(self, ):
        ''' 
        Implements a filtering fn for strava polyline data
        Strava GPS likes to 'blip' and show erroneous jumps
        Fn removes junk points to smooth out mapping in Tableau
        Typically a change in lat or change in lng >= +/-0.002 is erroneous
        '''
        
        df[['lat_diff', 'lng_diff']] = df[['lat', 'lng']].diff(axis=0)
        df_filtered = df[
            (abs(df['lat_diff']) <= 0.002 ) &
            (abs(df['lng_diff']) <= 0.002 )
        ]
        return df_filtered


    def generatePolylineDf(self, df):
        ''' Generate df for polyline data '''

        df_polyline = pd.DataFrame()
        df.reset_index(inplace=True)
        
        df['map'] = df['map'].astype(str) # cast to string to ensure hash
        for idx, grp in df.groupby(['id', 'timestamp', 'map']):
            decodedPolylineData = decodePolylineData(idx[2])
            df_run = pd.DataFrame(decodedPolylineData, columns=['lat', 'lng'])
            df_run.reset_index(inplace=True)
            df_run['timestamp'] = idx[1]
            df_run['id'] = idx[0]
            
            df_polyline = df_polyline.append(df_run)
        
        df_polyline_filtered = filterAnomalousPolylineData(df_polyline)
        return df_polyline_filtered