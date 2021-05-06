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

proc AutoFocusSel {} {
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

proc addrep {newstyle} {
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

proc RenderScene {} {
    color Display Background white
    display projection Orthographic
    axes location Off
    render TachyonInternal scene.tga /usr/bin/open %s
}
