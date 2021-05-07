proc AutoFocus { seltext } {
  set molid top
  set prog 1
  set me [lindex [info level [info level]] 0]

  set sel [atomselect $molid "$seltext"]
  set center [measure center $sel weight mass]
  $sel delete

  foreach molid [molinfo list] {
    eval "molinfo $molid set center [list [list $center]]"
  }

  set global_matrix [lindex [molinfo top get global_matrix] 0]
  set ctrans [list [lindex [lindex $global_matrix 0] 3] [lindex [lindex $global_matrix 1] 3] [lindex [lindex $global_matrix 2] 3]]
  set ntrans [vecscale $ctrans [expr pow(abs($prog-1.),$prog)]]
  eval "translate to $ntrans"
  return
}


proc AutoScaleAllVisible {{zoom_factor 1}} {
  set prog 1
  set me [lindex [info level [info level]] 0]
  #----
  set minX "false"
  set minY "false"
  set maxX "false"
  set maxY "false"
  set zoom [expr 1.8 * $zoom_factor]

  #compute bb for all visible stuff
  set mols [molinfo list]
  foreach molid $mols {
    if {[molinfo $molid get displayed] && [molinfo $molid get numframes] > 0} {
      set num_reps [molinfo $molid get numreps]
      if {$num_reps > 0} {
     set seltext ""
     for {set i 0} {$i<$num_reps} {incr i} {
       if {[mol showrep $molid $i]} {
         if {[string length $seltext] > 0} { set seltext "$seltext or " }
         set temp [molinfo $molid get "{selection $i}"]
         set seltext "${seltext}(${temp})"
       }
     }
      }
      if {[string length $seltext] > 0} {
     set sel [atomselect $molid ($seltext)]
     set mm [measure minmax $sel]
     $sel delete
     set minXtemp [lindex [lindex $mm 0] 0]
     set minYtemp [lindex [lindex $mm 0] 1]
     set maxXtemp [lindex [lindex $mm 1] 0]
     set maxYtemp [lindex [lindex $mm 1] 1]
     set minX [expr $minXtemp < $minX || $minX == "false" ? $minXtemp : $minX]
     set minY [expr $minYtemp < $minY || $minY == "false" ? $minYtemp : $minY]
     set maxX [expr $maxXtemp > $maxX || $maxX == "false" ? $maxXtemp : $maxX]
     set maxY [expr $maxYtemp > $maxY || $maxY == "false" ? $maxYtemp : $maxY]
      }
    }
  }
  if {$minX != "false"} {#true for 1 true for all
    set rangeX [expr $maxX - $minX]
    set rangeY [expr $maxY - $minY]
    set maxrange [expr max($rangeX,$rangeY)]
    set target [expr $zoom/$maxrange]
    set cscale [lindex [lindex [lindex [molinfo top get scale_matrix] 0] 0] 0]
    set nscale [expr $target + (($cscale - $target) * pow(abs($prog-1.),$prog))]
    eval "scale to $nscale"
  } else {
      puts "$me: nothing seems to be visible!"
  }
}

proc ZoomSel {} {
  global sel
  puts $sel

  set molid top
  set prog 1
  set me [lindex [info level [info level]] 0]

  set center [measure center $sel weight mass]

  foreach molid [molinfo list] {
    eval "molinfo $molid set center [list [list $center]]"
  }

  set global_matrix [lindex [molinfo top get global_matrix] 0]
  set ctrans [list [lindex [lindex $global_matrix 0] 3] [lindex [lindex $global_matrix 1] 3] [lindex [lindex $global_matrix 2] 3]]
  set ntrans [vecscale $ctrans [expr pow(abs($prog-1.),$prog)]]
  eval "translate to $ntrans"
  AutoScaleAllVisible 1.5
  return
}

proc addrep {sel newstyle} {
    global sel
    set molid top
    mol addrep $molid
    set repid [expr [molinfo $molid get numreps]-1]
    mol modselect $repid $molid [$sel text]
    mol modstyle $repid $molid $newstyle
}

proc changerep {newstyle} {
    set molid top
    set repid [expr [molinfo $molid get numreps]-1]
    mol modstyle $repid $molid $newstyle
}

proc Render {} {
    color Display Background white
    display projection Orthographic
    axes location Off
    render TachyonInternal scene.tga /usr/bin/open %s
}

#------------------------------------------------------------------
# $Id: remote_ctl.tcl,v 1.6 2003/02/12 21:33:11 oliver Exp $
# based on bounce.tcl and vmdcollab.tcl
# from http://www.ks.uiuc.edu/Research/vmd/script_library/scripts/vmdcollab/
#
# start this in VMD and send commands to the listening port to have VMD
# execute them remotely
# (also see http://www.tcl.tk/scripting/netserver.html)
#
# Usage: vmd -e remote_ctl.tcl
# or vmd> source remote_ctl.tcl
#
# Security: we only allow connections from localhost (see acpt)
#
# Bugs:
# * once a wrong command was sent, the connection appears
# to 'block' and does not accept correct commands later
# * does not write result back to socket (one way connection...) so
# there is no way to inquire objects in vmd

namespace eval remote_ctl {
variable main
variable clients
variable default_vmd_port
set default_vmd_port 5555
# I am too dumb to set the default value for port from
# $default_vmd_port so I put 5555 in there literally
proc start { {port %(PORT)} } {
variable main
set main [socket -server remote_ctl::acpt $port]
putlog "Listening on port $port"
}
proc acpt { sock addr port } {
variable clients
if {[string compare $addr "127.0.0.1"] != 0} {
putlog "Unauthorized connection attempt from $addr port $port"
close $sock
return
}
putlog "Accept $sock from $addr port $port"
set clients($sock) 1
fconfigure $sock -buffering line
fileevent $sock readable [list remote_ctl::recv $sock]
}
proc recv { sock } {
variable main
variable clients
if { [eof $sock] || [catch {gets $sock line}]} {
# end of file or abnormal connection drop:
# shut down this connection
close $sock
putlog "Closing $sock"
unset clients($sock)
} else {
if {[string compare $line "quit"] == 0} {
# prevent new connections
# existing connections stay open
# No -- Bug(?): 'quit' closes VMD...
putlog "Disallowing incoming connections by request of $sock"
close $main
}
# execute the received commands
# should check for runtime errors which otherwise leave the connection
# in an unusable state
# eval $line
set rc [catch $line result]
if { $rc } {
#puts $sock "Error executing comand '$line': n$result"
puts "Error executing comand '$line': $result"
} else {
#puts $sock $result
#puts $result
}
}
}
###### would like the last line from stdout in line ###########
# (or any working solution....)
proc send { sock line} {
variable clients
# send reply to connecting client
putlog "send '$line' to $sock"
puts $sock $line
}

proc putlog { text } {
puts $text
return
}
}

remote_ctl::putlog "Starting remote_ctl server in vmd: connect with something like"
remote_ctl::putlog "telnet localhost %(PORT)"
remote_ctl::start
