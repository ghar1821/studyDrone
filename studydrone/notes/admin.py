from django.contrib import admin
from notes.models import Course, Note, Rating, Tag, NoteTag, Rating, Comment, Group, Membership, Enhancement, Message, Attachment, SentMessage     

from notes.models import MaliciousReport

# bulk 1 ###############################################

class CourseAdmin(admin.ModelAdmin):
	list_display = ('id','code','title','credit_pt','description','sem')

# Bulk 2 ###############################################

class NoteAdmin(admin.ModelAdmin):
	list_display = ('id','download_count','download_cost','title','description','format','note_file','course','upload_time','permission_group','permission_public','uploader','extends')

class TagAdmin(admin.ModelAdmin):
	list_display = ('id','tag')

class NoteTagAdmin(admin.ModelAdmin):
	list_display = ('note','tag')

# Bulk 3 ###############################################

class RatingAdmin(admin.ModelAdmin):
	list_display = ('id','given_by','Note','rate','submission_time')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','given_by','Note','comment_content','submission_time')


# Bulk 4 ###############################################

class GroupAdmin(admin.ModelAdmin):
	list_display = ('id','name','description','created_since','creator')

class MembershipAdmin(admin.ModelAdmin):
	list_display = ('member','group')

# Bulk 5 ###############################################

class EnhancementAdmin(admin.ModelAdmin):
	list_display = ('id','description','reported_by','report_time','report_type')

# Bulk 6 ###############################################

class MessageAdmin(admin.ModelAdmin):
	list_display = ('id','title','body','message_time','sender')

class AttachmentAdmin(admin.ModelAdmin):
	list_display = ('id','file_attached')

class SentMessageAdmin(admin.ModelAdmin):
	list_display = ('message','receiver','attachment')

class MaliciousReportAdmin(admin.ModelAdmin):
	list_display = ('id','reported_by','note','report_content','submission_time')

admin.site.register(Course,CourseAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(NoteTag,NoteTagAdmin)
admin.site.register(Rating,RatingAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Group,GroupAdmin)
admin.site.register(Membership,MembershipAdmin)
admin.site.register(Enhancement,EnhancementAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Attachment,AttachmentAdmin)
admin.site.register(SentMessage,SentMessageAdmin)
admin.site.register(MaliciousReport,MaliciousReportAdmin)

