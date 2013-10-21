#! /bin/sh

if [ $# -lt 1 ] ; then
  echo "  Usage: image.sh directory_where_the_files_are name_of_generated_texfile number_of_images_per_slide mode"
  echo "  Generates name_of_generated_texfile.tex with number_of_images_per_slide by frame"
  echo "  If mode "alone" specified, file is compilable"
  exit 1
fi

dir=$1
name=$2
numpic=$3
mode=$4

if [ "${mode}" = "alone" ]; then
    echo "\documentclass[8pt]{beamer}" >> ${name}.tex
    echo "\usetheme{Boadilla}" >> ${name}.tex
    echo "\usepackage{graphicx}" >> ${name}.tex
    echo '\\'"begin{document}" >> ${name}.tex
fi

i1=-1
j1=0
all=`ls $dir/*eps | wc -l`
allok=`expr $all - 1`
for img in `ls $dir/*eps `
do

    if [ "$numpic" = "9" ]; then
        i1=`expr ${i1} + 1`
        j1=`expr ${i1} % 3`
        k1=`expr ${i1} % 9`
        
	    if [ "${k1}" = "0" ]; then
	        echo  '\\'"begin{frame}"  >> ${name}.tex
	        echo '\\'"begin{columns}" >> ${name}.tex
	    fi
	    if [ "$j1" = "0" ]; then
	        echo '\\'"begin{column}{4cm}" >> ${name}.tex
	    fi
        echo " \includegraphics[width=.97"'\\'"textwidth]{${img}}"'\\''\\' >> ${name}.tex
	    if [ "$j1" = "2" ]; then
	        echo '\\'"end{column}" >> ${name}.tex
	    fi
	    if [ "$k1" = "8" -o "$i1" = "$allok" ]; then
		    if [ "$j1" != "2" ]; then
		        echo '\\'"end{column}" >> ${name}.tex
		    fi
		    if [ "$j1" = 2 ]; then
		        echo "" >> ${name}.tex
                #		echo '\\'"vspace{12cm}" >> ${name}.tex
		        echo "" >> ${name}.tex
		    fi
	        echo '\\'"end{columns}" >> ${name}.tex
	        echo " \end{frame} " >> ${name}.tex 
	    fi
    fi
    
    if [ "$numpic" = "4" ]; then
        i1=`expr $i1 + 1`
        j1=`expr ${i1} % 2`
        j2=`expr ${i1} % 4`
        
	    if [ "$j2" = "0" ]; then
	        echo  '\\'"begin{frame}"  >> ${name}.tex
	        echo '\\'"begin{columns}" >> ${name}.tex
	    fi
	    if [ "$j1" = "0" ]; then
	        echo '\\'"begin{column}{6cm}" >> ${name}.tex
	    fi
        echo " \includegraphics[width=.97"'\\'"textwidth]{${img}}"'\\''\\' >> ${name}.tex
	    if [ "$j1" = "1" ]; then
	        echo '\\'"end{column}" >> ${name}.tex
	    fi
	    if [ "$j2" = "3" -o "$i1" = "$allok" ]; then
		    if [ "$j1" != "1" ]; then
		        echo '\\'"end{column}" >> ${name}.tex
		    fi
	        echo '\\'"end{columns}" >> ${name}.tex
	        echo " \end{frame} " >> ${name}.tex 
	    fi
    fi
    
    
done

if [ "$mode" = "alone" ]; then
    echo "\end{document}" >> ${name}.tex
fi

