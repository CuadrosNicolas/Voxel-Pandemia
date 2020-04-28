package main

import (

	"math"	
	"fmt"
	"time"
	"sync"
	"sort"
)

//Compute the number of infected during a specific day on a line
func suit(x float64, day float64, size float64) float64 {
	nDay := size - x
	if(day > nDay || day <= 0.0) {
		return 0
	} else if (day == 1) {
		return 1
	} else if (day - 1 <= x) {
		return 2
	} else {
		return 1
	}
}
//Simple memoisation functions
type memoryMap struct {
	mem map[float64]float64
}
func (mem *memoryMap) sliceMem(day float64, val float64) {
	mem.mem[day] = val
}

func (mem *memoryMap) getSliceMem(day float64) float64 {
	return mem.mem[day]
}

//Compute the number of infected during a specific day on a grid
func suit2d(yStart float64, xStart float64, day float64, size float64, mem* memoryMap) float64{
	
	//Verify if the result has not already appeared in a previous grid
	//due to time shift between grid
	memTmp := mem.getSliceMem(day)
	if memTmp != 0.0 {
		return memTmp
	}

	out := 0.0
	maxDay := size - yStart
	//Compute only the not finished line
	//May not be optimal and some variations appear depending if the size is odd or not
	if day <= maxDay {
		out += suit(xStart, day, size)
	}

	_max := day
	if day > maxDay {
		_max = maxDay
	}
	_min := 1.0
	if day > maxDay {
		_min = day - maxDay
	}

	for i:=_min; i<_max; i++ {
		localLineDay := day - math.Abs(i)
		tmp := suit(xStart, localLineDay, size)
		if yStart - i >= 0 {
			tmp *= 2
		}
		out += tmp
	}

	mem.sliceMem(day,out)

	return out
}

//Compute the number of infected during a specific day on a cube
func suit3d(zStart float64, yStart float64, xStart float64, day float64, size float64,mem* memoryMap) float64{
	out := 0.0
	lenghtZ := (size -zStart)
	maxDay := (size - yStart) + (size - xStart) - 1

	//Same optimization as the suit2d
	if day <= maxDay {
		out += suit2d(yStart, xStart, day, size,mem)
	}

	_max := day
	if day > lenghtZ {
		_max = lenghtZ
	}
	_min := 1.0
	if day - maxDay >= 2 {
		_min = day - maxDay
	}

	for i:=_min; i<_max; i++ {
		localSliceDay := day - math.Abs(i)
		tmp := suit2d(yStart, xStart, localSliceDay, size, mem)
		if zStart - i >= 0 {
			tmp *= 2
		}
		out += tmp
	}


	return out
}

//Return how the viruses progress depending on the first infected position
func getProgression(x float64, y float64, z float64, size float64) []float64 {
	mem := &memoryMap{map[float64]float64{}}
	day := 1.0
	addedPerDay := []float64{1}
	for true {
		day += 1
		tmp := suit3d(z,y,x,day,size,mem)
		if tmp > 0.0 {
			addedPerDay = append(addedPerDay, tmp)
		} else {
			break
		}
	}
	return addedPerDay
}

//Coordinates holder
type coordinates struct {
	x float64
	y float64
	z float64
}
//Return all possible combination of distinct coordinates giving distinct sequences
func getTranslation(size float64) []coordinates {
	out := []coordinates{}
	
	for i:=0.0;i<size/2;i++ {
		for j:=0.0;j<i+1;j++ {
			for k:=0.0;k<j+1;k++ {
				out = append(out, coordinates{i,j,k})
			}
		}
	}

	return out
}

//Virus progression holder
type result struct {
	sequences []float64
	coordinate coordinates
	index int
}

//Format result informations
func (res result) infos() string{
	seqString := "["
	for i,c := range(res.sequences) {
		seqString += fmt.Sprintf("%1.0f",c)
		if i < len(res.sequences) -1 {
			seqString += ", "
		} else {
			seqString += "]"
		}
	}
	translationString := fmt.Sprintf("[%1.0f, %1.0f, %1.0f]",res.coordinate.x,res.coordinate.y,res.coordinate.z)
	return fmt.Sprintf("Sequence : %s\nTranslation : %s",seqString,translationString)
}

//String padding from : https://play.golang.org/p/zciRZvD0Gr
func PadRight(str, pad string, lenght int) string {
	for {
		str += pad
		if len(str) > lenght {
			return str[0:lenght]
		}
	}
}

//Print results in a fancy table
func (res result) fancyPrint(size float64) {
	title := "| Jour | Total | Contamination | Pourcentage de contamination |"
	fmt.Println(res.infos())
	line := PadRight("","-",len(title))
	fmt.Println(line)
	fmt.Println(title)
	fmt.Println(line)
	count := 0.0
	percChar := "%"
	for i,v := range(res.sequences) {
		count += v
		countThisDay := v
		percentage := (count/(size*size*size))*100.0
		pr := fmt.Sprintf("| %s | %s | %s | %s |",
				PadRight(fmt.Sprintf("%1d",i+1)," ",len("Jour")),
				PadRight(fmt.Sprintf("%1.0f",count)," ",len("Total")),
				PadRight(fmt.Sprintf("%1.0f",countThisDay)," ",len("Contamination")),
				PadRight(fmt.Sprintf("%3.2f%s",percentage,percChar)," ",len("Pourcentage de contamination")))
		fmt.Println(pr)
		fmt.Println(line)
	}
	println()

}

type ConfFile struct {
	cubeSize 	    float64
	limitOne 	bool 
}

func main() {


	//Size of the cube
	size := 5.0
	//Get all possible translations
	translations := getTranslation(size)
	//Defines wait groups and channel for parrallel computing
	wg := sync.WaitGroup{}
    ch := make(chan result, len(translations))
	//Start the time
	start := time.Now()
	//For each translation compute the result and send it to the channel
	for i,v := range(translations) {
		wg.Add(1)
		go func(v coordinates, wg *sync.WaitGroup,index int) {
			ch <- result{getProgression(v.x,v.y,v.z,size),v,index}
			wg.Done()
		}(v, &wg,i)
	}
	wg.Wait()
	close(ch)
	//Sort the result in the order of their position in the translations array
	ordered := []result{}
	elapsed := time.Since(start)
	for res := range ch {
		ordered = append(ordered,res)
	}
	sort.SliceStable(ordered, func(i,j int) bool {
		return ordered[i].index < ordered[j].index
	})
	//Print all results
	for _,res := range(ordered) {
		res.fancyPrint(size)
	}
	fmt.Printf("Total groups : %d\n",len(translations))
	//Show the elapsed time
	fmt.Printf("Elapsed time : %s\n",elapsed)
}