package main

import (	
	"fmt"
	"sync"
	"sort"
	"encoding/json"
	"io/ioutil"
	"os"
	"time"
	"flag"
)

//Compute the number of infected during a specific day on a line
func suit(x int, day int, size int) int {
	nDay := size - x
	if(day > nDay || day <= 0) {
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
	mem map[int]int
}
func (mem *memoryMap) sliceMem(day int, val int) {
	mem.mem[day] = val
}

func (mem *memoryMap) getSliceMem(day int) int {
	return mem.mem[day]
}

//Compute the number of infected during a specific day on a grid
func suit2d(yStart int, xStart int, day int, size int, mem* memoryMap) int{
	
	//Verify if the result has not already appeared in a previous grid
	//due to time shift between grid
	memTmp := mem.getSliceMem(day)
	if memTmp != 0 {
		return memTmp
	}
	
	out := 0
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
	_min := 1
	if day > maxDay {
		_min = day - maxDay
	}

	for i:=_min; i<_max; i++ {
		localLineDay := day - i
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
func suit3d(zStart int, yStart int, xStart int, day int, size int,mem* memoryMap) int{
	out := 0
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
	_min := 1
	if day - maxDay >= 2 {
		_min = day - maxDay
	}

	for i:=_min; i<_max; i++ {
		localSliceDay := day - i
		tmp := suit2d(yStart, xStart, localSliceDay, size, mem)
		if zStart - i >= 0 {
			tmp *= 2
		}
		out += tmp
	}


	return out
}

//Return how the viruses progress depending on the first infected position
func getProgression(x int, y int, z int, size int) []int {
	mem := &memoryMap{map[int]int{}}
	day := 1
	addedPerDay := []int{1}
	for true {
		day += 1
		tmp := suit3d(z,y,x,day,size,mem)
		if tmp > 0 {
			addedPerDay = append(addedPerDay, tmp)
		} else {
			break
		}
	}
	return addedPerDay
}

//Coordinates holder
type coordinates struct {
	x int
	y int
	z int
}
//Return all possible combination of distinct coordinates giving distinct sequences
func getTranslation(size int) []coordinates {
	out := []coordinates{}
	
	for i:=0.0;i<float64(size)/2.0;i++ {
		for j:=0.0;j<i+1;j++ {
			for k:=0.0;k<j+1;k++ {
				out = append(out, coordinates{int(i),int(j),int(k)})
			}
		}
	}

	return out
}

//Virus progression holder
type result struct {
	sequences []int
	coordinate coordinates
	index int
}

//Format result informations
func (res result) infos() string{
	seqString := "["
	for i,c := range(res.sequences) {
		seqString += fmt.Sprintf("%d",c)
		if i < len(res.sequences) -1 {
			seqString += ", "
		} else {
			seqString += "]"
		}
	}
	translationString := fmt.Sprintf("[%d, %d, %d]",res.coordinate.x,res.coordinate.y,res.coordinate.z)
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
func (res result) fancyPrint(size int) {
	title := "| Jour | Total | Contamination | Pourcentage de contamination |"
	fmt.Println(res.infos())
	line := PadRight("","-",len(title))
	fmt.Println(line)
	fmt.Println(title)
	fmt.Println(line)
	count := 0
	percChar := "%"
	for i,v := range(res.sequences) {
		count += v
		countThisDay := v
		percentage := (float64(count)/(float64(size)*float64(size)*float64(size)))*100.0
		pr := fmt.Sprintf("| %s | %s | %s | %s |",
				PadRight(fmt.Sprintf("%d",i+1)," ",len("Jour")),
				PadRight(fmt.Sprintf("%d",count)," ",len("Total")),
				PadRight(fmt.Sprintf("%d",countThisDay)," ",len("Contamination")),
				PadRight(fmt.Sprintf("%3.2f%s",percentage,percChar)," ",len("Pourcentage de contamination")))
		fmt.Println(pr)
		fmt.Println(line)
	}

}

type ConfFile struct {
	CubeSize 	    int `json:"size"`
	LimitOne 	bool  `json:"limit"`
}

func main() {

	verbose := flag.Bool("v",false,"Print all results")
	flag.Parse()
	conf := ConfFile{}
	jsonConf, _ := os.Open("conf.json")
	byteValue, _ := ioutil.ReadAll(jsonConf)
	json.Unmarshal(byteValue,&conf)
 	//Size of the cube
	size := conf.CubeSize
	//Get all possible translations
	translations := getTranslation(size)
	//Defines wait groups and channel for parrallel computing
	wg := sync.WaitGroup{}
	ch := make(chan result, len(translations))
	//Start the timer
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
	
	elapsed := time.Since(start)
	if  *verbose {
		//In case of verbose print the result
		//Sort the result in the order of their position in the translations array
		ordered := []result{}
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
	}
	fmt.Printf("Total groups : %d\n",len(translations))
	//Show the elapsed time
	fmt.Printf("Elapsed time : %s\n",elapsed)
}