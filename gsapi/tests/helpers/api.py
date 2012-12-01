    def InsertCnt(self, _c, data, verbose=True):
        dumps_data = dumps(data)
        print "<pre>requests.post('http://" + self.host + '/' + _c + "', data='" + dumps_data + "')</pre>"

        rs = self.app.post('/'+_c, data=dumps_data)

        err = "\nInsertCnt of %s FAILED!" % _c

        if rs.status == 200:
            data = json.loads(rs.data)
            doc = data['docs'][0]['doc']
            m = getattr(models, _c)(**doc)
            if verbose:
                print m.dNam

            return m
        elif rs.status == 400:
            data = json.loads(rs.data)
            print err
            print data['errors'][0]['errors']
            print
            assert False
        else:
            print err
            assert False