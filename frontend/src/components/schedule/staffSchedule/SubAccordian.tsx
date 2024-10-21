import { Employee, EmployeeLocation } from "@/app/schedule/api"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@radix-ui/react-accordion"
import { flName } from "./StaffAccordian"

interface ISubAccordian {
    employees: flName[]
    employeeLocations: EmployeeLocation[]
}



const SubAccordian: React.FC<ISubAccordian> = ({ employees, employeeLocations }) => {
    return (
        <Accordion type="single" collapsible>
            <AccordionItem value='item-1' >
                <AccordionTrigger>
                    Other Teams Under Me
                </AccordionTrigger>
                <AccordionContent>
                    { }
                </AccordionContent>
            </AccordionItem>
        </Accordion>)
}
export default SubAccordian