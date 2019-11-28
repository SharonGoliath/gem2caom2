# -*- coding: utf-8 -*-
# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2019.                            (c) 2019.
#  Government of Canada                 Gouvernement du Canada
#  National Research Council            Conseil national de recherches
#  Ottawa, Canada, K1A 0R6              Ottawa, Canada, K1A 0R6
#  All rights reserved                  Tous droits réservés
#
#  NRC disclaims any warranties,        Le CNRC dénie toute garantie
#  expressed, implied, or               énoncée, implicite ou légale,
#  statutory, of any kind with          de quelque nature que ce
#  respect to the software,             soit, concernant le logiciel,
#  including without limitation         y compris sans restriction
#  any warranty of merchantability      toute garantie de valeur
#  or fitness for a particular          marchande ou de pertinence
#  purpose. NRC shall not be            pour un usage particulier.
#  liable in any event for any          Le CNRC ne pourra en aucun cas
#  damages, whether direct or           être tenu responsable de tout
#  indirect, special or general,        dommage, direct ou indirect,
#  consequential or incidental,         particulier ou général,
#  arising from the use of the          accessoire ou fortuit, résultant
#  software.  Neither the name          de l'utilisation du logiciel. Ni
#  of the National Research             le nom du Conseil National de
#  Council of Canada nor the            Recherches du Canada ni les noms
#  names of its contributors may        de ses  participants ne peuvent
#  be used to endorse or promote        être utilisés pour approuver ou
#  products derived from this           promouvoir les produits dérivés
#  software without specific prior      de ce logiciel sans autorisation
#  written permission.                  préalable et particulière
#                                       par écrit.
#
#  This file is part of the             Ce fichier fait partie du projet
#  OpenCADC project.                    OpenCADC.
#
#  OpenCADC is free software:           OpenCADC est un logiciel libre ;
#  you can redistribute it and/or       vous pouvez le redistribuer ou le
#  modify it under the terms of         modifier suivant les termes de
#  the GNU Affero General Public        la “GNU Affero General Public
#  License as published by the          License” telle que publiée
#  Free Software Foundation,            par la Free Software Foundation
#  either version 3 of the              : soit la version 3 de cette
#  License, or (at your option)         licence, soit (à votre gré)
#  any later version.                   toute version ultérieure.
#
#  OpenCADC is distributed in the       OpenCADC est distribué
#  hope that it will be useful,         dans l’espoir qu’il vous
#  but WITHOUT ANY WARRANTY;            sera utile, mais SANS AUCUNE
#  without even the implied             GARANTIE : sans même la garantie
#  warranty of MERCHANTABILITY          implicite de COMMERCIALISABILITÉ
#  or FITNESS FOR A PARTICULAR          ni d’ADÉQUATION À UN OBJECTIF
#  PURPOSE.  See the GNU Affero         PARTICULIER. Consultez la Licence
#  General Public License for           Générale Publique GNU Affero
#  more details.                        pour plus de détails.
#
#  You should have received             Vous devriez avoir reçu une
#  a copy of the GNU Affero             copie de la Licence Générale
#  General Public License along         Publique GNU Affero avec
#  with OpenCADC.  If not, see          OpenCADC ; si ce n’est
#  <http://www.gnu.org/licenses/>.      pas le cas, consultez :
#                                       <http://www.gnu.org/licenses/>.
#
#  $Revision: 4 $
#
# ***********************************************************************
#

import os
import shutil
from datetime import date
from mock import patch, Mock

from caom2pipe import manage_composable as mc
from gem2caom2 import validator

import gem_mocks


@patch('cadcdata.core.net.BaseWsClient.post')
@patch('cadcutils.net.ws.WsCapabilities.get_access_url')
def test_validator(caps_mock, tap_mock):
    caps_mock.return_value = 'https://sc2.canfar.net/sc2repo'
    tap_response = Mock()
    tap_response.status_code = 200
    tap_response.iter_content.return_value = \
        [b'<?xml version="1.0" encoding="UTF-8"?>\n'
         b'<VOTABLE xmlns="http://www.ivoa.net/xml/VOTable/v1.3" '
         b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         b'version="1.3">\n'
         b'<RESOURCE type="results">\n'
         b'<INFO name="QUERY_STATUS" value="OK" />\n'
         b'<INFO name="QUERY_TIMESTAMP" value="2019-11-14T16:26:46.274" />\n'
         b'<INFO name="QUERY" value="SELECT distinct A.uri&#xA;FROM '
         b'caom2.Observation as O&#xA;JOIN caom2.Plane as P on O.obsID = '
         b'P.obsID&#xA;JOIN caom2.Artifact as A on P.planeID = A.planeID&#xA;'
         b'WHERE O.collection = \'GEMINI\'&#xA;" />\n'
         b'<TABLE>\n'
         b'<FIELD name="uri" datatype="char" arraysize="*" '
         b'utype="caom2:Artifact.uri" xtype="uri">\n'
         b'<DESCRIPTION>external URI for the physical artifact</DESCRIPTION>\n'
         b'</FIELD>\n'
         b'<DATA>\n'
         b'<TABLEDATA>\n'
         b'<TR>\n'
         b'<TD>gemini:GEM/S20170102S0663.fits</TD>\n'
         b'</TR>\n'
         b'<TR>\n'
         b'<TD>gemini:GEM/S20170102S0663.jpg</TD>\n'
         b'</TR>\n'
         b'<TR>\n'
         b'<TD>gemini:GEM/N20120102S0663.fits</TD>\n'
         b'</TR>\n'
         b'<TR>\n'
         b'<TD>gemini:GEM/N20120102S0663.jpg</TD>\n'
         b'</TR>\n'
         b'<TR>\n'
         b'<TD>gemini:GEM/N20191102S0665.fits</TD>\n'
         b'</TR>\n'
         b'<TR>\n'
         b'<TD>gemini:GEM/N20191102S0665.jpg</TD>\n'
         b'</TR>\n'
         b'</TABLEDATA>\n'
         b'</DATA>\n'
         b'</TABLE>\n'
         b'<INFO name="QUERY_STATUS" value="OK" />\n'
         b'</RESOURCE>\n'
         b'</VOTABLE>\n']

    ad_response = Mock()
    ad_response.status_code = 200
    ad_response.iter_content.return_value = \
        [b'<?xml version="1.0" encoding="UTF-8"?>\n'
         b'<VOTABLE xmlns="http://www.ivoa.net/xml/VOTable/v1.3" '
         b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         b'version="1.3">\n'
         b'<RESOURCE type="results">\n'
         b'<INFO name="QUERY_STATUS" value="OK" />\n'
         b'<INFO name="QUERY_TIMESTAMP" value="2019-11-27T00:07:08.736" />\n'
         b'<INFO name="QUERY" value="SELECT ingestDate, fileName&#xA;FROM '
         b'archive_files&#xA;WHERE archiveName = \'NEOSS\'&#xA;AND '
         b'fileName = \'xEOS_SCI_2019319035900.fits\'" />\n'
         b'<TABLE>\n'
         b'<FIELD name="ingestDate" datatype="char" arraysize="*" '
         b'xtype="timestamp">\n'
         b'<DESCRIPTION>file ingest date</DESCRIPTION>\n'
         b'</FIELD>\n'
         b'<FIELD name="fileName" datatype="char" arraysize="255*">\n'
         b'<DESCRIPTION>file name</DESCRIPTION>\n'
         b'</FIELD>\n'
         b'<DATA>\n'
         b'<TABLEDATA />\n'
         b'</DATA>\n'
         b'</TABLE>\n'
         b'<INFO name="QUERY_STATUS" value="OK" />\n'
         b'</RESOURCE>\n'
         b'</VOTABLE>\n']

    global count
    count = 0

    def _mock_return():
        global count
        if count == 0:
            count = 1
            return tap_response
        else:
            return ad_response

    tap_mock.return_value.__enter__.side_effect = _mock_return

    if not os.path.exists('/usr/src/app/cadcproxy.pem'):
        with open('/usr/src/app/cadcproxy.pem', 'w') as f:
            f.write('proxy content')

    getcwd_orig = os.getcwd
    os.getcwd = Mock(return_value=gem_mocks.TEST_DATA_DIR)
    try:
        test_subject = validator.GeminiValidator()
        test_listing_fqn = \
            f'{test_subject._config.working_directory}/{mc.VALIDATE_OUTPUT}'
        if os.path.exists(test_listing_fqn):
            os.unlink(test_listing_fqn)
        if os.path.exists(test_subject._config.work_fqn):
            os.unlink(test_subject._config.work_fqn)

        test_rejected = f'{gem_mocks.TEST_DATA_DIR}/validate/' \
                        f'test_rejected.yml'
        import logging
        logging.error(f'test_rejected {test_rejected}, rejected_fqn '
                      f'{test_subject._config.rejected_fqn}')
        shutil.copy(test_rejected, test_subject._config.rejected_fqn)

        test_source, test_meta, test_data = test_subject.validate()
        assert test_source is not None, 'expected source result'
        assert len(test_source) == 1037, 'wrong number of source results'
        assert 'rS20111124S0053.fits' in test_source, 'wrong result content'
        assert 'rS20111124S0053.jpg' in test_source, 'wrong result content'

        assert test_meta is not None, 'expected destination result'
        assert len(test_meta) == 2, 'wrong # of destination results'
        assert 'S20170102S0663.fits' in test_meta, \
            'wrong destination content'
        assert os.path.exists(test_listing_fqn), 'should create file record'

        test_subject.write_todo()
        assert os.path.exists(test_subject._config.work_fqn), \
            'should create file record'
        with open(test_subject._config.work_fqn, 'r') as f:
            content = f.readlines()
        content_sorted = sorted(content)
        assert content_sorted[0] == '02jul07.0034.fits\n', 'wrong content'

        # assert False
    finally:
        os.getcwd = getcwd_orig


def test_date_file_name():
    getcwd_orig = os.getcwd
    os.getcwd = Mock(return_value=gem_mocks.TEST_DATA_DIR)
    try:
        # because randomness in naming
        fnames = ['S20170905S0318.fits', 'rgS20130103S0098_FRINGE.jpg',
                  'GS20141226S0203_BIAS.fits', 'mrgS20160901S0122_add.jpg',
                  'N20160403S0236_flat_pasted.fits', 'N20141109S0266_BIAS',
                  'TX20170321_red.2507.fits', 'N20170616S0540.fits',
                  '02jul07.0186.fits', 'GN2001BQ013-04.fits',
                  '2002APR23_591.fits', 'r01dec05_007.fits',
                  'p2004may20_0048_FLAT.fits', 'P2003JAN14_0148_DARK.fits',
                  'ag2003feb19_6.0001.fits', '02jun25.0071.fits']
        validate = validator.GeminiValidator()
        for f_name in fnames:
            result = validate._date_file_name(f_name)
            assert isinstance(result, date), f'{f_name}'
    finally:
        os.getcwd = getcwd_orig
