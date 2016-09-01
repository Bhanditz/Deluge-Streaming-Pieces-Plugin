#
# priority_thread.py
#
# Copyright (C) 2010 Nick Lanham <nick@afternight.org>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.

from deluge.ui.client import client
import deluge.component as component

__target_priority = [7, 5, 2]
__last_first = {}

def priority_loop(meth):
    torrents = meth()
    for t in torrents:	# Run this for every torrent
        tor = component.get("TorrentManager").torrents[t]	# Get some more info of the torrent?
        if tor.status.state == tor.status.downloading: # Only look at downloading torrents
            lf = __last_first.get(t)	# Find previous lf for this torrent
            if not(lf):					# If there was no previous one,
                lf = 0					# Set to 0? wtf? Wouldn't it already be False?
            try:
                cand = tor.status.pieces.index(False,lf)	# cand = piece status
                if (tor.handle.piece_priority(cand) == 0):	#
                    prios = tor.handle.piece_priorities()	# prios = list of priorities
                    while (tor.handle.piece_priority(cand) == 0): 
                        cand += 1		# Increment some counter
                        pcand = 0		# Reset something relating to this counter
                        for (i,x) in enumerate(prios[cand:]):	# priorities starting at cand
                            if x > 0:	# If piece is desired
                                pcand = i + cand	# set pcand to
                                break
                        cand = max(tor.status.pieces.index(False,cand), pcand)
                lf = cand
            except ValueError:
                continue
            # lf is now the first un-downloaded, desired piece of this torrent
            next_ones = []				# Init list of pieces starting at lf
            for i in range(60):
            	piece = lf + i
            	if i < 10:
            		target_priority = 7
            	if i >= 10 and i < 30:
            		target_priority = 5
            	if i >= 30:
            		target_priority = 2
            	try:
            		if (tor.handle.piece_priority(piece) < target_priority):
            			tor.handle.piece_priority(piece, target_priority)
            	except Exception as e:
            		print('DrewError: ' + e)
            __last_first[t] = lf
