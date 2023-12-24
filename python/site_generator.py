import sheetdata as sheetdata
import css_maps_gen
import other_maps_gen
import test_mapname_filename_match
import test_drive_matches_sheet
import write_screenshots_to_sheet

TESTS_ENABLED = False
WRITE_TO_SHEET = False

def main():
    data = sheetdata.get_data()
    collapsible_with_dl, collapsible_no_dl = create_collapsible(data)
    css_dl, css_no_dl, other_dl, other_no_dl, = split_map_by_game(collapsible_with_dl, collapsible_no_dl)
    css_maps_gen.build(css_dl, css_no_dl)
    other_maps_gen.build(other_dl, other_no_dl)

def create_collapsible(data):
    collapsible_list_dl = []
    collapsible_list_no_dl = []

    map_name_index = 0
    link_index = 6
    img_index = 7

    for row in data[1:]:  # Skip the header row
        content = []
        has_dl = False

        # this could be done by setting variables to each index without a second for loop and the if statements
        # but this way feels a little more readable to me
        
        for index, item in enumerate(row[0:], start=0): 
            column_header = data[0][index]

            if index == map_name_index:
                map_name = item

            elif index == link_index and "drive.google.com" in item:
                # Handle links for the specified index
                drive_link_from_sheet = item
                site_link = f'<a href="{drive_link_from_sheet}">{map_name}.zip</a>' # don't feel like calling drive api every time to get file type.  it's always zip for
                content.append(f'<b>{column_header}:</b><br />&emsp;{site_link}') 
                has_dl = True
            
            elif index == link_index and "drive.google.com" not in item:
                has_dl = False

            elif index == img_index and "drive.google.com" in item:
                # Handle images with missing or error alt text for the specified index
                img_alt = f'{map_name}'
                img_link = f'<img src="{item}" alt="{img_alt}" class="ImgThumbnail" loading="lazy">'
                content.append(f'<b>screenshot:</b><br />&emsp;{img_link}')
                site_link = (f'<b>site link:</b><br />&emsp;<a href="#{map_name}">{map_name}</a>')
                content.append(site_link) # screnshot is last thing processed, and we want the site link after that.

            else:
                # Handle regular content
                content.append(f'<b>{column_header}:</b><br />&emsp;{item}') # noted above, data[0] = column header name

        content_html = '<br />'.join(content)
        collapsible_html = f'\n<div id="{map_name}">\n\t<button type="button" class="collapsible">{map_name}</button>\n\t<div id="{map_name}" class="content"><p>{content_html}</p></div>\n</div>'
        # This line is a little absurd
        # JS found in collapsible_handler.js utilizes the nested divs with the same name
        # if a jump link is followed to a matching map name, the JS expands that collapsible.

        if has_dl:
            collapsible_list_dl.append(collapsible_html)
        else:
            collapsible_list_no_dl.append(collapsible_html)

    return collapsible_list_dl, collapsible_list_no_dl

def split_map_by_game(collapsible_list_dl, collapsible_list_no_dl):
    collapsible_list_css_dl = []
    collapsible_list_css_no_dl = []
    collapsible_list_1p6_dl = []
    collapsible_list_1p6_no_dl = []

    for item in range(len(collapsible_list_dl)):
        if "CSS" in collapsible_list_dl[item]:
            collapsible_list_css_dl.append(collapsible_list_dl[item])
        else:
            collapsible_list_1p6_dl.append(collapsible_list_dl[item])
    
    for item in range(len(collapsible_list_no_dl)):
        if "CSS" in collapsible_list_no_dl[item]:
            collapsible_list_css_no_dl.append(collapsible_list_no_dl[item])
        else:
            collapsible_list_1p6_no_dl.append(collapsible_list_no_dl[item])
    
    return collapsible_list_css_dl, collapsible_list_css_no_dl, collapsible_list_1p6_dl, collapsible_list_1p6_no_dl

if __name__ == '__main__':
    if WRITE_TO_SHEET == True:
        print("Writing links to all screenshots in drive to sheet")
        write_screenshots_to_sheet.generate_rows_with_screenshot()
    main()
    if TESTS_ENABLED == True:
        print("Testing if all drive files have sheet entry")
        test_drive_matches_sheet.get_downloads_for_missing_maps(WRITE_TO_SHEET) # this is confusing, maybe split into a test and a write
        print("Testing if all mapnames match filenames for downloads")
        test_mapname_filename_match.check_names()
        print("all done with tests!!")
    else:
        print("no tests, all done")