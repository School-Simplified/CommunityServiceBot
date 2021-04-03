from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from shutil import copyfile
import discord
from core.common import *
import textwrap
import re
from core.common import *

config, _ = load_config()

async def self2(StudentName, StudnetID, SchoolName, SchoolPhone,StudentAddress,StudentCity,StudentState, StudentEmail, stuffdone, ctx, DiscID, supervisor):
    copyfile("PDFbase.pdf", fr"PDF/rec-{DiscID}.pdf")
    open(fr"PDF/rec-{DiscID}.pdf")
    

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Times-Roman", 10)


    #Top:
    can.drawString(146, 647, StudentName)
    can.drawString(380, 647, StudnetID)
    can.drawString(115, 627, SchoolName)
    can.drawString(353, 627, SchoolPhone)
    can.drawString(157, 605, StudentAddress)
    can.drawString(345, 605, StudentCity)
    can.drawString(455, 605, StudentState)
    can.drawString(110, 585, StudentEmail)
    
    #Bottom:
    can.drawString(185, 185, config['OrgName'])
    can.drawString(370, 185, config['OrgCity'])
    can.drawString(462, 185, config['OrgState'])

    AdultName, Email, PhoneNumber = getValues(supervisor)
    can.drawString(130, 165, PhoneNumber)
    can.drawString(325, 165, Email)
    #can.drawString(247, 105, "Signature")
    can.drawString(145, 145, AdultName)

    yVal = 505
    content = textwrap.fill(stuffdone, 110)
    for x in content.splitlines():
        lineContent = '\n'.join(line.strip() for line in re.findall(r'.{1,40}(?:\s+|$)', x))
        try:
            lineContent = lineContent.replace("\u00A0","\u0020")
        except:
            print("Error Code 1")
        finally:
            print(lineContent)
            can.drawString(75, yVal, lineContent)
            yVal = yVal - 20
    
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open("PDFbase.pdf", "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    outputStream = open(fr"PDF/rec-{DiscID}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()


    await ctx.send(file=discord.File(fr"PDF/rec-{DiscID}.pdf"))


async def doBottom(Date, AdultName ,userID, DiscID, self):
    copyfile(fr"PDF/rec-{DiscID}.pdf", fr"PDF/rec2-{DiscID}.pdf")
    open(fr"PDF/rec2-{DiscID}.pdf")
    user = await self.bot.fetch_user(userID)
    Requster = await self.bot.fetch_user(DiscID)
    

    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Times-Roman", 10)


    can.drawString(245, 102, AdultName)
    can.drawString(440, 102, Date)

    can.drawString(180, 83, AdultName)
    can.drawString(380, 83, Date)

    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open(fr"PDF/rec-{DiscID}.pdf", "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    outputStream = open(fr"PDF/rec2-{DiscID}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    await user.send("**YOU HAVE APPROVED THEIR REQUEST!**\nHere is your copy of their PDF!")
    await user.send(file=discord.File(fr'PDF/rec2-{DiscID}.pdf'))

    embed = discord.Embed(title = "Authorization Approved", description = "Dear User, your community service request has been approved by your supervisor and below attached is your signed Community Service PDF.", color = 0x34eb71)
    await Requster.send(embed = embed)
    await Requster.send(file=discord.File(fr'PDF/rec2-{DiscID}.pdf'))



async def DMPDF(StudentName, StudnetID, SchoolName, SchoolPhone,StudentAddress,StudentCity,StudentState, StudentEmail, stuffdone, self, DiscID, supervisor):
    copyfile("PDFbase.pdf", rf"PDF/rec-{DiscID}.pdf")
    open(rf"PDF/rec-{DiscID}.pdf")


    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Times-Roman", 10)


    #Top:
    can.drawString(146, 647, StudentName)
    can.drawString(380, 647, StudnetID)
    can.drawString(115, 627, SchoolName)
    can.drawString(353, 627, SchoolPhone)
    can.drawString(157, 605, StudentAddress)
    can.drawString(345, 605, StudentCity)
    can.drawString(455, 605, StudentState)
    can.drawString(110, 585, StudentEmail)
    
    #Bottom:
    can.drawString(185, 185, config['OrgName'])
    can.drawString(370, 185, config['OrgCity'])
    can.drawString(462, 185, config['OrgState'])

    AdultName, Email, PhoneNumber = getValues(supervisor)
    can.drawString(130, 165, PhoneNumber)
    can.drawString(325, 165, Email)
    #can.drawString(247, 105, "Signature")
    can.drawString(145, 145, AdultName)

    yVal = 505
    content = textwrap.fill(stuffdone, 110)
    for x in content.splitlines():
        lineContent = '\n'.join(line.strip() for line in re.findall(r'.{1,40}(?:\s+|$)', x))
        try:
            lineContent = lineContent.replace("\u00A0","\u0020")
        except:
            print("Error Code 1")
        finally:
            print(lineContent)
            can.drawString(75, yVal, lineContent)
            yVal = yVal - 20
    
    

    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open("PDFbase.pdf", "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    outputStream = open(rf"PDF/rec-{DiscID}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    user = await self.bot.fetch_user(450476337954553858)
    await user.send(f"New Response from {StudentName}:")
    await user.send(file=discord.File(rf"PDF/rec-{DiscID}.pdf"))

    guild = self.bot.get_guild(805593783684562965)
    channel = guild.get_channel(813109417267429386)
    await channel.send(f"PDF for {StudentName}:")
    await channel.send(file=discord.File(rf"PDF/rec-{DiscID}.pdf"))

    
async def givePDF(StudentName, StudnetID, SchoolName, SchoolPhone,StudentAddress,StudentCity,StudentState, StudentEmail, stuffdone, self, DiscID, supervisor):
    copyfile("PDFbase.pdf", fr"PDF/rec-{DiscID}.pdf")
    open(fr"PDF/rec-{DiscID}.pdf")
    

    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Times-Roman", 10)


    #Top:
    can.drawString(146, 647, StudentName)
    can.drawString(380, 647, StudnetID)
    can.drawString(115, 627, SchoolName)
    can.drawString(353, 627, SchoolPhone)
    can.drawString(157, 605, StudentAddress)
    can.drawString(345, 605, StudentCity)
    can.drawString(455, 605, StudentState)
    can.drawString(110, 585, StudentEmail)
    
    #Bottom:
    can.drawString(185, 185, config['OrgName'])
    can.drawString(370, 185, config['OrgCity'])
    can.drawString(462, 185, config['OrgState'])

    AdultName, Email, PhoneNumber = getValues(supervisor)
    can.drawString(130, 165, PhoneNumber)
    can.drawString(325, 165, Email)
    #can.drawString(247, 105, "Signature")
    can.drawString(145, 145, AdultName)

    yVal = 505
    content = textwrap.fill(stuffdone, 110)
    for x in content.splitlines():
        lineContent = '\n'.join(line.strip() for line in re.findall(r'.{1,40}(?:\s+|$)', x))
        try:
            lineContent = lineContent.replace("\u00A0","\u0020")
        except:
            print("Error Code 1")
        finally:
            print(lineContent)
            can.drawString(75, yVal, lineContent)
            yVal = yVal - 20
    
    

    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open("PDFbase.pdf", "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    outputStream = open(rf"PDF/rec-{DiscID}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
